"""Digital Twin Backend - FastAPI Application."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .config import load_config
from .middleware import LocalOnlyMiddleware
from .core.rate_limit import rate_limit_middleware

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

app.add_middleware(LocalOnlyMiddleware)


@app.middleware("http")
async def rate_limit_handler(request: Request, call_next):
    await rate_limit_middleware(request)
    return await call_next(request)


# Lazy-load API routers — gracefully skip if dependencies are missing
_router_modules = [
    ("auth", "auth_api"),
    ("profile", "profile_api"),
    ("chat", "chat_api"),
    ("knowledge", "knowledge_api"),
    ("voice", "voice_api"),
    ("evolution", "evolution_api"),
]

for module_name, _ in _router_modules:
    try:
        mod = __import__(f"backend.app.api.{module_name}", fromlist=["router"])
        if hasattr(mod, "router"):
            app.include_router(mod.router)
            logger.info(f"✅ Loaded API: {module_name}")
        else:
            logger.warning(f"⚠️  No router in {module_name}")
    except ImportError as e:
        logger.warning(f"⚠️  Skipping {module_name}: {e}")

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

@app.get("/")
async def root():
    return {"message": "Digital Twin API", "docs": "/docs"}
