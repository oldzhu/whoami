from pydantic import BaseModel
from typing import Optional, List, Dict


class Document(BaseModel):
    id: str
    filename: str
    file_type: str
    size_bytes: int
    chunk_count: int = 0
    uploaded_at: str


class KnowledgeChunk(BaseModel):
    id: str
    document_id: str
    content: str
    embedding: Optional[List[float]] = None
    metadata: Dict = {}


class SearchQuery(BaseModel):
    query: str
    top_k: int = 5
    filters: Optional[Dict[str, str]] = None


class SearchResult(BaseModel):
    chunk_id: str
    content: str
    score: float
    document_id: str
