"""Self-evolution API — pending fact review and approval."""
from fastapi import APIRouter, Depends
from ..core.evolution import ReviewQueue, KnowledgeUpdater
from ..middleware import auth_required

router = APIRouter(prefix="/api/evolution", tags=["evolution"])

_queue = ReviewQueue()
_updater = KnowledgeUpdater()


@router.get("/pending")
async def get_pending(username: str = Depends(auth_required)):
    return {"facts": _queue.get_pending()}


@router.post("/approve/{fact_id}")
async def approve_fact(fact_id: str, username: str = Depends(auth_required)):
    _queue.approve(fact_id)
    _updater.apply_approved()
    return {"status": "approved", "fact_id": fact_id}


@router.post("/reject/{fact_id}")
async def reject_fact(fact_id: str, username: str = Depends(auth_required)):
    _queue.reject(fact_id)
    return {"status": "rejected", "fact_id": fact_id}
