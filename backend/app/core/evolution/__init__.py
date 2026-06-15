"""Self-evolution engine - extract facts, review, and update knowledge base."""

from .extractor import FactExtractor
from .review_queue import ReviewQueue
from .knowledge_updater import KnowledgeUpdater
from .graph_updater import GraphUpdater

__all__ = ["FactExtractor", "ReviewQueue", "KnowledgeUpdater", "GraphUpdater"]
