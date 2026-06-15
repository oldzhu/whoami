"""Model registry and management."""
import yaml
from pathlib import Path
from typing import List, Dict, Optional
from ..models.config import ModelConfig


class ModelRegistry:
    """Registry of configured LLM models."""

    def __init__(self, config_path: str = "models/config.yaml"):
        self.config_path = Path(config_path)
        self._models: List[ModelConfig] = []
        self._routing: Dict = {}
        self._load()

    def _load(self):
        if self.config_path.exists():
            with open(self.config_path) as f:
                data = yaml.safe_load(f) or {}
            for m in data.get("models", []):
                self._models.append(ModelConfig(**m))
            self._routing = data.get("routing", {})

    def list_models(self, model_type: Optional[str] = None) -> List[ModelConfig]:
        if model_type:
            return [m for m in self._models if m.type == model_type]
        return self._models

    def get_model(self, name: str) -> Optional[ModelConfig]:
        for m in self._models:
            if m.name == name:
                return m
        return None

    def get_routing(self, key: str) -> Optional[str]:
        return self._routing.get(key)

    @property
    def chat_models(self) -> List[ModelConfig]:
        return self.list_models("chat")

    @property
    def embedding_models(self) -> List[ModelConfig]:
        return self.list_models("embedding")
