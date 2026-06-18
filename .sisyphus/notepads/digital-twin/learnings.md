# Learnings

## Docker Containerization (Task 30)

- Backend entrypoint: `uvicorn app.main:app --host 0.0.0.0 --port 8000`, health check at `/health`
- Web uses Next.js 16 with Tailwind 4, no `package-lock.json` exists (used `npm install` instead of `npm ci`)
- `curl` installed in backend image for healthcheck support (python:3.11-slim doesn't include it)
- Web does not import from `shared/` directory
- Config is at project root (`config.yaml`), mounted as volume

## Mock LLM Adapter (Task: mock-adapter)

- Created `backend/app/core/llm/mock_adapter.py` — full `LLMProvider` implementation with canned responses
- Updated factory `create_llm_provider()` to support `backend="mock"` and fallback to MockAdapter for unknown/unreachable backends
- MockAdapter implements all 5 abstract methods: `chat`, `stream`, `embed`, `models`, `ping`
- `_generate_response()` uses keyword matching against Chinese and English terms for realistic replies
- Embed returns 384-dim float vectors (matching common local embedding model dimensions)
- Python binary is `/usr/bin/python3` (not `python`)

## Data Management System (Task: data-management)

- Auth uses SHA256 via hashlib (simple, local-only) — stored in `data/auth.json` as `{username, password_hash}`
- Sessions are in-memory dict (uuid4 tokens), lost on restart — OK for localhost-only use
- `LocalOnlyMiddleware` checks both `X-Forwarded-For` header and `request.client.host` against LOCAL_IPS set
- `AuthRequired` dependency uses FastAPI's HTTPBearer for extracting Bearer token from Authorization header
- Protected prefixes: `/api/auth`, `/api/settings`, `/api/admin` (middleware applied at global level)
- Profile GET is public; PUT/POST require auth; profile loads from `data/profile.json` if exists, falls back to DEFAULT_PROFILE
- Voice speaker upload: POST /api/voice/speaker with multipart WAV file, saves to `data/voice/`
- Venv Python: `/home/oldzhu/whoami/venv/bin/python` (not system `python` or `python3`)
- Frontend uses Next.js 16 with App Router, all pages are client components (`'use client'`)
- ESLint `react-hooks/set-state-in-effect` rule is strict — setState in useEffect is flagged; use useState lazy initializer instead
- ESLint `react-hooks/refs` — ref.current assignment must happen inside useEffect, not during render
- Session storage (sessionStorage) used for auth token persistence (not localStorage — per Next.js/React conventions)
