# Learnings

## Docker Containerization (Task 30)

- Backend entrypoint: `uvicorn app.main:app --host 0.0.0.0 --port 8000`, health check at `/health`
- Web uses Next.js 16 with Tailwind 4, no `package-lock.json` exists (used `npm install` instead of `npm ci`)
- `curl` installed in backend image for healthcheck support (python:3.11-slim doesn't include it)
- Web does not import from `shared/` directory
- Config is at project root (`config.yaml`), mounted as volume
