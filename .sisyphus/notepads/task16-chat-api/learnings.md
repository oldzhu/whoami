## Task 16: Chat API Endpoints

### Patterns & Conventions
- Lazy singleton pattern for service initialization (_get_router, _get_rag, _get_sessions, _get_memory)
- FastAPI APIRouter with prefix="/api/chat" groups all chat endpoints
- WebSocket uses json.dumps for sending typed messages (thinking/token/done)
- ConversationMemory requires SessionManager instance in constructor

### Key Decisions
- Adapted plan code to match actual component APIs:
  - ConversationMemory(session_manager) — requires SessionManager arg
  - RAGChain(backend="auto") and ModelRouter(backend="auto") use "auto" default
  - SessionManager(db_path="data/sessions.db") uses default path
- Registered router in main.py via `app.include_router(chat_api.router)`
- Updated api/__init__.py to import chat module
