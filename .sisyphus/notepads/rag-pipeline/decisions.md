# RAG Pipeline - Decisions

## Graph Search Implementation
Instead of the stub `_graph_search` from the plan, implemented a functional heuristic:
- Extracts candidate terms from query (skip stopwords, short terms <3 chars)
- Tries each as skill name via GraphStore.query_related_people()
- Also tries as person name via get_person() → queries skills and projects
- Scores based on skill level and availability of data

## BM25 Scoring
BM25Scorer uses simple TF normalization (not full IDF) since we don't maintain a global document corpus. k1=1.5, b=0.75 parameters per standard BM25 defaults.

## Reranker Strategy
MVP uses heuristic term-overlap scoring (0.5 * original_score + 0.5 * overlap_count). Can be replaced with cross-encoder model later by swapping `_model` implementation in `__init__`.

## LLM Fallback
RAGChain.query() catches LLM exceptions and returns partial results with error message rather than failing entirely.
