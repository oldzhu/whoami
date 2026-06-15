"""Fallback strategies for model routing."""
import logging

logger = logging.getLogger(__name__)


class FallbackStrategy:
    """Handles model unavailability gracefully."""

    @staticmethod
    def should_retry(error: Exception) -> bool:
        """Determine if a request should be retried."""
        error_str = str(error).lower()
        retryable = ["timeout", "connection", "unavailable", "503", "502", "429"]
        return any(r in error_str for r in retryable)

    @staticmethod
    def get_alternative_model(failed_model: str, available_models: list) -> str:
        """Pick an alternative model from available ones."""
        if available_models:
            return available_models[0]
        return "qwen2.5:7b"
