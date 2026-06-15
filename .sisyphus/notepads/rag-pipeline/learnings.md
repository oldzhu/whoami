# RAG Pipeline - Learnings

## Component Design
- **HybridRetriever**: Combines 3 retrieval strategies (vector, BM25, graph) with RRF fusion
- **Reranker**: Heuristic term-overlap scoring; upgradeable to cross-encoder model
- **ContextBuilder**: Formats retrieved chunks with source citations into LLM-ready messages
- **RAGChain**: Orchestrates retrieve->rerank->build->generate pipeline

## Integration Points
- VectorStore.search() returns `[{id, text, score, metadata}]` - passed through as-is
- GraphStore.graph methods: `query_related_people(skill)`, `query_person_skills(name)`, `query_person_projects(name)`, `get_person(name)`
- LocalEmbedder.embed_query() returns `List[float]`
- create_llm_provider() returns LLMProvider with async `chat()` and `stream()`

## Graph Search Heuristic
- Tokenize query, filter stopwords, try each term as skill name via `query_related_people`
- Also try as person name via `get_person` + `query_person_skills` + `query_person_projects`
- Score graph results based on skill level

## RRF Fusion
- `rrf_score = score + 1/(rank + 60)` - standard Reciprocal Rank Fusion
- Deduplication by `id` or `text` content
