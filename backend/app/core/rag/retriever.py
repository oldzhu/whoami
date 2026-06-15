"""Hybrid retrieval: vector + BM25 + graph traversal."""

import re
from math import log
from typing import Any, Dict, List, Optional

from ..ingestion.embedder import LocalEmbedder
from ..storage.graph_store import GraphStore
from ..storage.vector_store import VectorStore


class BM25Scorer:
    """Simple BM25-like keyword scorer with TF normalization."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b

    def tokenize(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    def score(self, query: str, document: str) -> float:
        query_terms = self.tokenize(query)
        doc_terms = self.tokenize(document)
        if not doc_terms:
            return 0.0
        score = 0.0
        for term in query_terms:
            tf = doc_terms.count(term) / len(doc_terms)
            score += tf
        return score / max(len(query_terms), 1)


class HybridRetriever:
    """Combines vector search, BM25 keyword search, and graph traversal."""

    def __init__(self, collection_name: str = "knowledge_base"):
        self.vector_store = VectorStore()
        self.graph_store = GraphStore()
        self.embedder = LocalEmbedder()
        self.bm25 = BM25Scorer()
        self.collection_name = collection_name

    def search(
        self,
        query: str,
        top_k: int = 5,
        use_vector: bool = True,
        use_bm25: bool = True,
        use_graph: bool = True,
    ) -> List[Dict[str, Any]]:
        """Hybrid search combining multiple retrieval methods."""
        results: List[Dict[str, Any]] = []

        # 1. Vector search
        if use_vector:
            try:
                query_embedding = self.embedder.embed_query(query)
                vector_results = self.vector_store.search(
                    self.collection_name,
                    query_embedding,
                    top_k=top_k,
                )
                for r in vector_results:
                    r["source"] = "vector"
                    r["score"] = r.get("score", 0)
                results.extend(vector_results)
            except Exception:
                pass

        # 2. BM25 keyword search — score the top vector results plus any extra docs
        if use_bm25:
            bm25_scored = []
            candidate_pool = (
                results[: top_k * 2]
                if results
                else [{"text": query, "source": "bm25", "score": 0.0}]
            )
            for r in candidate_pool:
                bm25_score = self.bm25.score(query, r.get("text", ""))
                bm25_scored.append({**r, "bm25_score": bm25_score, "source": "bm25"})
            bm25_scored.sort(key=lambda x: x["bm25_score"], reverse=True)
            results.extend(bm25_scored[:top_k])

        # 3. Graph traversal
        if use_graph:
            try:
                graph_results = self._graph_search(query)
                results.extend(graph_results[:top_k])
            except Exception:
                pass

        # Deduplicate and fuse scores via Reciprocal Rank Fusion
        return self._fuse_results(results, top_k)

    def _graph_search(self, query: str) -> List[Dict[str, Any]]:
        """Search knowledge graph for relevant entities matching query terms."""
        results: List[Dict[str, Any]] = []
        query_lower = query.lower()
        terms = set(re.findall(r"\w+", query_lower))

        # Heuristic: extract single-word potential skill names from the query
        # (skip very short/common words)
        stopwords = {
            "what", "is", "the", "a", "an", "in", "on", "at", "to", "for",
            "of", "and", "or", "has", "have", "did", "do", "does", "can",
            "you", "your", "my", "me", "i", "are", "was", "were", "be",
            "tell", "about", "how", "which", "who", "where", "when",
        }
        candidate_skills = {t for t in terms if len(t) > 2 and t not in stopwords}

        # Try each candidate as a skill name
        for skill in candidate_skills:
            try:
                related = self.graph_store.query_related_people(skill)
                for entry in related:
                    results.append(
                        {
                            "text": f"{entry.get('person', '')} has skill {skill} "
                            f"at level {entry.get('level', 'N/A')}",
                            "source": "graph",
                            "score": 0.5 + (entry.get("level", 0) / 20.0),
                            "metadata": entry,
                        }
                    )
            except Exception:
                continue

            # Also check if any person has this skill
            try:
                person_data = self.graph_store.get_person(skill.title())
                if person_data:
                    person_skills = self.graph_store.query_person_skills(skill.title())
                    person_projects = self.graph_store.query_person_projects(
                        skill.title()
                    )
                    context_lines = []
                    if person_skills:
                        skills_str = ", ".join(
                            f"{s.get('skill', '')}(L{s.get('level', '')})"
                            for s in person_skills
                        )
                        context_lines.append(f"Skills: {skills_str}")
                    if person_projects:
                        proj_str = ", ".join(
                            p.get("project", "") for p in person_projects
                        )
                        context_lines.append(f"Projects: {proj_str}")
                    if context_lines:
                        results.append(
                            {
                                "text": " | ".join(context_lines),
                                "source": "graph",
                                "score": 0.7,
                                "metadata": {
                                    "person": skill.title(),
                                    "skills": person_skills,
                                    "projects": person_projects,
                                },
                            }
                        )
            except Exception:
                continue

        return results

    def _fuse_results(
        self, results: List[Dict[str, Any]], top_k: int
    ) -> List[Dict[str, Any]]:
        """Reciprocal Rank Fusion: combine multiple ranked lists."""
        seen: Dict[str, Dict[str, Any]] = {}
        for rank, r in enumerate(results):
            rid = r.get("id", r.get("text", ""))
            if rid in seen:
                continue
            r["rrf_score"] = r.get("score", 0) + (1.0 / (rank + 60))
            seen[rid] = r

        fused = sorted(
            seen.values(), key=lambda x: x.get("rrf_score", 0), reverse=True
        )
        return fused[:top_k]
