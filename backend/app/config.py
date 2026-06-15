"""Configuration management for Digital Twin backend."""
import os
from pathlib import Path
import yaml
from pydantic import BaseModel

class LLMConfig(BaseModel):
    backend: str = "auto"
    models_dir: str = "./models"

class HardwareConfig(BaseModel):
    cuda: bool = True
    rocm: bool = True
    cann: bool = True

class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

class DataConfig(BaseModel):
    dir: str = "./data"
    chroma_dir: str = "./data/chroma"

class AppConfig(BaseModel):
    llm: LLMConfig = LLMConfig()
    hardware: HardwareConfig = HardwareConfig()
    server: ServerConfig = ServerConfig()
    data: DataConfig = DataConfig()

def load_config(config_path: str = "config.yaml") -> AppConfig:
    """Load configuration from YAML file, with env var overrides."""
    config_file = Path(config_path)
    if config_file.exists():
        with open(config_file) as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}
    if os.getenv("LLM_BACKEND"):
        data.setdefault("llm", {})["backend"] = os.getenv("LLM_BACKEND")
    if os.getenv("API_PORT"):
        data.setdefault("server", {})["port"] = int(os.getenv("API_PORT"))
    return AppConfig(**data)
