# Learnings

- config.yaml hardware values must be proper YAML booleans (true/false), not strings like "enabled", to match pydantic `bool` fields in HardwareConfig.
- PYTHONPATH must include the backend directory for `from backend.app.main import app` to resolve when running from project root.
- Uvicorn startup validates lifespan config loading immediately; any pydantic validation error crashes startup.
