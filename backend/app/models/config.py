from pydantic import BaseModel
from typing import List, Optional


class ModelConfig(BaseModel):
    name: str
    provider: str  # "ollama" | "llamacpp" | "vllm"
    type: str  # "chat" | "embedding" | "reranker"
    quant: Optional[str] = None
    size_gb: float
    languages: List[str]
    tags: List[str]
    description: Optional[str] = None
    recommended_hardware: List[str] = []
    min_ram_gb: Optional[float] = None


class LLMProvider(BaseModel):
    backend: str  # "cuda" | "rocm" | "cann" | "cpu" | "auto"
    models: List[ModelConfig]
    base_url: str
    api_type: str  # "openai" | "ollama" | "custom"
