"""Digital Twin Backend - FastAPI Application."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import load_config
from .api import knowledge as knowledge_api
from .api import chat as chat_api
from .api import profile as profile_api
from .api import voice as voice_api
from .api import evolution as evolution_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Digital Twin backend starting...")
    config = load_config()
    app.state.config = config
    logger.info(f"LLM backend: {config.llm.backend}")
    yield
    logger.info("Digital Twin backend shutting down...")

app = FastAPI(
    title="Digital Twin API",
    description="AI Digital Twin - Local OSS LLM-powered personal clone",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(knowledge_api.router)

app.include_router(chat_api.router)

app.include_router(profile_api.router)

app.include_router(voice_api.router)

app.include_router(evolution_api.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

@app.get("/")
async def root():
    return {"message": "Digital Twin API", "docs": "/docs"}
