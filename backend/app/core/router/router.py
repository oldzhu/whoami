"""Multi-model routing engine."""
import logging
from typing import Dict, Optional

from ..llm import create_llm_provider, LLMProvider
from ..model_manager import ModelRegistry
from .classifier import IntentClassifier

logger = logging.getLogger(__name__)


class ModelRouter:
    """Routes messages to the best available model."""

    def __init__(self, backend: str = "auto"):
        self.provider: LLMProvider = create_llm_provider(backend)
        self.registry = ModelRegistry()
        self.classifier = IntentClassifier()
        self._model_cache: Dict[str, bool] = {}

    async def route(self, message: str) -> str:
        """Determine which model to use for a message."""
        scores = self.classifier.classify(message)
        logger.debug(f"Classification scores: {scores}")

        if scores.get("code", 0) > 0.5:
            model = self.registry.get_routing("code_chat")
        elif scores.get("chinese", 0) > 0.5:
            model = self.registry.get_routing("chinese_chat")
        elif scores.get("casual", 0) > 0.5:
            model = self.registry.get_routing("english_chat")
        else:
            model = self.registry.get_routing("default_chat")

        if model is None:
            model = self.registry.get_routing("default_chat") or "qwen2.5:7b"

        if model not in self._model_cache:
            try:
                available_models = await self.provider.models()
                self._model_cache = {m: True for m in available_models}
            except Exception:
                pass

        if not self._model_cache.get(model, False):
            return self._get_fallback(model)

        return model

    def _get_fallback(self, preferred: str) -> str:
        """Get a fallback model if preferred is unavailable."""
        fallback_order = [
            self.registry.get_routing("default_chat"),
            self.registry.get_routing("chinese_chat"),
            self.registry.get_routing("english_chat"),
            "qwen2.5:7b",
            "llama3.1:8b",
        ]
        for fb in fallback_order:
            if fb and fb != preferred and self._model_cache.get(fb, True):
                logger.warning(
                    "Model '%s' unavailable, falling back to '%s'", preferred, fb
                )
                return fb
        return preferred

    def get_embedding_model(self) -> str:
        return self.registry.get_routing("default_embedding") or "all-minilm:l6-v2"
