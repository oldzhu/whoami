"""Knowledge base management API."""
import os
import uuid
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import List, Optional
from ..core.ingestion import IngestionPipeline
from ..core.storage import VectorStore
from ..middleware import auth_required

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

_pipeline = None
_vector_store = None

def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        _pipeline = IngestionPipeline()
    return _pipeline

def _get_store():
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
        _vector_store.create_collection("knowledge_base")
    return _vector_store

class UploadResponse(BaseModel):
    task_id: str
    filename: str
    chunks: int
    status: str

class DocumentInfo(BaseModel):
    id: str
    filename: str
    chunks: int
    uploaded_at: str

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...), username: str = Depends(auth_required)):
    """Upload a document to the knowledge base."""
    allowed_extensions = {".pdf", ".docx", ".md", ".txt"}
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(400, f"Unsupported file type: {ext}")

    upload_dir = "data/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    safe_name = f"{uuid.uuid4().hex[:8]}_{os.path.basename(file.filename or 'upload')}"
    filepath = os.path.join(upload_dir, safe_name)
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)

    pipeline = _get_pipeline()
    chunks = pipeline.ingest_file(filepath)

    store = _get_store()
    texts = [c["text"] for c in chunks]
    embeddings = [c["embedding"] for c in chunks]
    metadatas = [{"source_file": file.filename, "chunk_index": i} for i in range(len(chunks))]
    store.add_documents("knowledge_base", texts, embeddings, metadatas)

    task_id = str(uuid.uuid4())
    return UploadResponse(
        task_id=task_id,
        filename=file.filename or "unknown",
        chunks=len(chunks),
        status="completed",
    )

@router.get("/documents")
async def list_documents(username: str = Depends(auth_required)):
    """List all documents in the knowledge base."""
    store = _get_store()
    count = store.count("knowledge_base")
    return {"document_count": "N/A (chunk-level)", "total_chunks": count}

@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str, username: str = Depends(auth_required)):
    return {"status": "deleted", "id": doc_id}

@router.get("/search")
async def search_knowledge(q: str = Query(...), top_k: int = 5):
    """Semantic search the knowledge base."""
    from ..core.ingestion.embedder import LocalEmbedder
    embedder = LocalEmbedder()
    query_embedding = embedder.embed_query(q)
    store = _get_store()
    results = store.search("knowledge_base", query_embedding, top_k=top_k)
    return {"query": q, "results": results}

@router.get("/stats")
async def get_stats(username: str = Depends(auth_required)):
    """Get knowledge base statistics."""
    store = _get_store()
    return {
        "total_chunks": store.count("knowledge_base"),
        "collections": store.list_collections(),
    }
