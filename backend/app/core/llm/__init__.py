"""LLM abstraction layer."""
from .base import LLMProvider
from .ollama_adapter import OllamaAdapter
from .llamacpp_adapter import LlamaCppAdapter
from .vllm_adapter import VLLMAdapter
from .mock_adapter import MockAdapter
import subprocess
import os
from typing import Optional

__all__ = ["LLMProvider", "OllamaAdapter", "LlamaCppAdapter", "VLLMAdapter", "MockAdapter", "create_llm_provider", "detect_hardware_backend"]


def detect_hardware_backend() -> str:
    """Auto-detect available hardware backend."""
    try:
        subprocess.run(["nvidia-smi"], capture_output=True, check=True)
        return "cuda"
    except (FileNotFoundError, PermissionError, subprocess.CalledProcessError):
        pass
    try:
        subprocess.run(["rocm-smi"], capture_output=True, check=True)
        return "rocm"
    except (FileNotFoundError, PermissionError, subprocess.CalledProcessError):
        pass
    if os.path.exists("/usr/local/Ascend"):
        return "cann"
    return "cpu"


def create_llm_provider(backend: str = "auto", **kwargs) -> LLMProvider:
    """Factory: create an LLM provider based on backend type."""
    if backend == "mock":
        return MockAdapter(**kwargs)
    if backend == "auto":
        backend = detect_hardware_backend()
    base_url = kwargs.get("base_url", "http://localhost:11434")
    if backend == "ollama" or backend in ("cuda", "rocm", "cann", "cpu"):
        try:
            return OllamaAdapter(base_url=base_url)
        except Exception:
            return MockAdapter(**kwargs)
    elif backend == "llamacpp":
        try:
            return LlamaCppAdapter(base_url=base_url)
        except Exception:
            return MockAdapter(**kwargs)
    elif backend == "vllm":
        try:
            return VLLMAdapter(base_url=base_url)
        except Exception:
            return MockAdapter(**kwargs)
    else:
        return MockAdapter(**kwargs)
