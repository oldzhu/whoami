"""Auto-update Neo4j knowledge graph from approved facts."""
import logging
from typing import Any, Dict, List

from .review_queue import ReviewQueue
from ..storage.graph_store import GraphStore

logger = logging.getLogger(__name__)


class GraphUpdater:
    """Updates the knowledge graph with approved facts from evolution."""

    def __init__(self) -> None:
        self.review_queue = ReviewQueue()
        self.graph_store = GraphStore()

    def apply_pending_updates(self) -> Dict[str, Any]:
        approved = self.review_queue.get_approved()

        nodes_added = 0
        relationships_added = 0
        conflicts: List[Dict[str, Any]] = []

        for fact in approved:
            result = self._apply_fact(dict(fact))
            nodes_added += result.get("nodes", 0)
            relationships_added += result.get("relationships", 0)
            if result.get("conflict"):
                conflicts.append(result["conflict"])

        logger.info(
            "Graph updated: +%d nodes, +%d relationships, %d conflicts",
            nodes_added,
            relationships_added,
            len(conflicts),
        )

        return {
            "nodes_added": nodes_added,
            "relationships_added": relationships_added,
            "conflicts": conflicts,
        }

    def _apply_fact(self, fact: Dict[str, Any]) -> Dict[str, Any]:
        fact_type = fact.get("fact_type", "other")
        content = fact.get("content", "")
        result: Dict[str, Any] = {"nodes": 0, "relationships": 0}

        try:
            if fact_type == "skill":
                skill_name = content.replace("Knows ", "").replace("knows ", "").strip()
                if skill_name:
                    self.graph_store.add_skill("DigitalTwin", skill_name)
                    result["nodes"] = 1
                    result["relationships"] = 1

            elif fact_type == "project":
                project_name = (
                    content.replace("Worked on: ", "").replace("worked on: ", "").strip()
                )
                if project_name:
                    self.graph_store.add_project("DigitalTwin", project_name)
                    result["nodes"] = 1
                    result["relationships"] = 1

            elif fact_type == "experience":
                self.graph_store.add_project("DigitalTwin", content[:100])
                result["nodes"] = 1
                result["relationships"] = 1

        except Exception as e:
            logger.warning("Failed to apply fact to graph: %s", e)
            result["conflict"] = str(e)

        return result

    def check_conflicts(self, facts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        conflicts: List[Dict[str, Any]] = []
        existing_skills: set[str] = set()

        try:
            person_data = self.graph_store.get_person("DigitalTwin")
            if person_data:
                skills = self.graph_store.query_person_skills("DigitalTwin")
                existing_skills = {s.get("skill", "").lower() for s in skills}
        except Exception:
            pass

        for fact in facts:
            if fact.get("fact_type") == "skill":
                skill_name = fact.get("content", "").replace("Knows ", "").lower()
                if skill_name in existing_skills:
                    conflicts.append({
                        "fact": fact,
                        "type": "duplicate",
                        "message": f"Skill '{skill_name}' already exists",
                    })

        return conflicts
