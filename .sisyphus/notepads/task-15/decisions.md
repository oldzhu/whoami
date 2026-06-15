## Decisions

- **SQLite via stdlib sqlite3**: Chosen for MVP simplicity. DB path configurable via constructor, defaults to `data/sessions.db`. Auto-creates directory and tables.
- **UUID4 hex strings**: Used for session and message IDs — simple, unique, no external deps.
- **Context window via char-count**: `estimate_tokens` uses `chars // 4` as rough heuristic. Good enough for MVP.
- **Compression = truncation**: `ContextCompressor.compress` keeps most recent messages that fit. `summarize` returns a count/size placeholder — not a real LLM summary (MVP scope).
- **Memory always prepends system prompt**: `prepare_context` includes the system prompt as first message, then recent messages from DB, trimming oldest to stay within max_tokens.

## Patterns

- Followed existing codebase conventions: module-level docstrings, type hints, Path from pathlib, standard library imports.
- `SessionManager` follows same pattern as `ModelRegistry` — init with config path, load/cache internally.
- Context manager for sqlite connections ensures proper cleanup.