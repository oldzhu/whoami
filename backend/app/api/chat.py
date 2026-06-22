"""Chat API endpoints."""
import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from ..core.router import ModelRouter
from ..core.rag import RAGChain
from ..core.conversation import SessionManager, ConversationMemory
from ..middleware import auth_required

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])

_model_router = None
_rag_chain = None
_session_manager = None
_memory = None


def _get_router():
    global _model_router
    if _model_router is None:
        _model_router = ModelRouter()
    return _model_router


def _get_rag():
    global _rag_chain
    if _rag_chain is None:
        _rag_chain = RAGChain()
    return _rag_chain


def _get_sessions():
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager


def _get_memory():
    global _memory
    if _memory is None:
        _memory = ConversationMemory(_get_sessions())
    return _memory


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    model: str


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message and get an AI response."""
    sessions = _get_sessions()
    rag = _get_rag()
    router_ = _get_router()

    session_id = request.session_id or sessions.create_session()

    model_name = await router_.route(request.message)

    result = await rag.query(request.message)

    sessions.add_message(session_id, "user", request.message)
    sessions.add_message(session_id, "assistant", result["answer"])

    return ChatResponse(
        response=result["answer"],
        session_id=session_id,
        model=model_name,
    )


@router.websocket("/ws")
async def chat_websocket(websocket: WebSocket):
    """Real-time streaming chat via WebSocket."""
    await websocket.accept()
    sessions = _get_sessions()
    rag = _get_rag()
    session_id = sessions.create_session()

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            message = msg.get("message", "")

            if not message:
                continue

            sessions.add_message(session_id, "user", message)

            await websocket.send_text(json.dumps({"type": "thinking"}))

            full_response = ""
            async for token in rag.stream(message):
                full_response += token
                await websocket.send_text(json.dumps({"type": "token", "content": token}))

            sessions.add_message(session_id, "assistant", full_response)

            await websocket.send_text(json.dumps({
                "type": "done",
                "session_id": session_id,
            }))

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected: %s", session_id)


@router.get("/history/{session_id}")
async def get_history(session_id: str, username: str = Depends(auth_required)):
    """Get message history for a session."""
    sessions = _get_sessions()
    session = sessions.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
