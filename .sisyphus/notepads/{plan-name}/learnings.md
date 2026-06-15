## Task 13: Neo4j Knowledge Graph

- Created `graph_store.py` with lazy driver initialization via `@property`
- All credentials sourced from env vars: `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`
- Cypher queries use MERGE (idempotent) pattern for node/edge creation
- Docker Compose snippet embedded as file header comments (per task requirement)
- neo4j 6.2.0 installed; requirement pinned to `>=5.0.0`
