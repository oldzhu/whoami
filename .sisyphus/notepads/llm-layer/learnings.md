# Learnings - LLM Inference Abstraction Layer

## Patterns Used
- **Abstract base class** (`LLMProvider`) with 5 methods: chat, stream, embed, models, ping
- **Adapter pattern**: Each backend (Ollama, llama.cpp, vLLM) wraps its HTTP API behind the common interface
- **Factory pattern**: `create_llm_provider()` selects adapter based on backend name or auto-detection
- **Graceful degradation**: All methods return empty/false on connection failure rather than raising

## Error Handling
- All adapters use aiohttp with try/except around HTTP calls
- Failed requests return sensible defaults: empty choices, empty embeddings, empty model list, False ping
- Log warnings on failures via `logging.getLogger(__name__)`

## Key Details
- Ollama uses its native REST API (/api/chat, /api/embeddings, /api/tags)
- llama.cpp and vLLM share OpenAI-compatible endpoints (/v1/chat/completions, /v1/embeddings, /v1/models)
- Stream parsing: Ollama uses NDJSON (readline), llama.cpp/vLLM use SSE (data: chunks)
- Hardware detection catches PermissionError in addition to FileNotFoundError
