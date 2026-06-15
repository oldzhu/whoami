# Docker Compose snippet for Neo4j:
#   neo4j:
#     image: neo4j:5
#     ports:
#       - "7474:7474"
#       - "7687:7687"
#     environment:
#       - NEO4J_AUTH=neo4j/password
#     volumes:
#       - neo4j_data:/data
#       - neo4j_logs:/logs
#   volumes:
#     neo4j_data:
#     neo4j_logs:

"""Neo4j knowledge graph store."""

import os
from typing import Any, Dict, List, Optional

from neo4j import GraphDatabase, basic_auth


class GraphStore:
    """Knowledge graph store using Neo4j."""

    def __init__(
        self,
        uri: str = None,
        user: str = None,
        password: str = None,
    ):
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "password")
        self._driver = None

    @property
    def driver(self):
        if self._driver is None:
            self._driver = GraphDatabase.driver(
                self.uri,
                auth=basic_auth(self.user, self.password),
            )
        return self._driver

    def close(self):
        if self._driver:
            self._driver.close()
            self._driver = None

    def _run(self, query: str, **params) -> List[Dict]:
        with self.driver.session() as session:
            result = session.run(query, **params)
            return [dict(record) for record in result]

    # === Person ===

    def create_person(self, name: str, properties: Dict = None) -> Dict:
        props = properties or {}
        result = self._run(
            "MERGE (p:Person {name: $name}) SET p += $props RETURN p",
            name=name,
            props=props,
        )
        return result[0] if result else {}

    def get_person(self, name: str) -> Optional[Dict]:
        result = self._run(
            "MATCH (p:Person {name: $name}) RETURN p", name=name
        )
        return result[0] if result else None

    # === Project ===

    def add_project(
        self,
        person_name: str,
        project_name: str,
        technologies: List[str] = None,
    ) -> Dict:
        techs = technologies or []
        result = self._run(
            """
            MERGE (p:Person {name: $person_name})
            MERGE (proj:Project {name: $project_name})
            MERGE (p)-[:WORKED_ON]->(proj)
            RETURN proj
            """,
            person_name=person_name,
            project_name=project_name,
        )
        for tech in techs:
            self._run(
                """
                MATCH (proj:Project {name: $project_name})
                MERGE (t:Technology {name: $tech})
                MERGE (proj)-[:USES]->(t)
                """,
                project_name=project_name,
                tech=tech,
            )
        return result[0] if result else {}

    # === Skills ===

    def add_skill(
        self, person_name: str, skill_name: str, level: int = 5
    ) -> Dict:
        result = self._run(
            """
            MERGE (p:Person {name: $person_name})
            MERGE (s:Skill {name: $skill_name})
            MERGE (p)-[r:HAS_SKILL]->(s)
            SET r.level = $level
            RETURN p, s, r
            """,
            person_name=person_name,
            skill_name=skill_name,
            level=level,
        )
        return result[0] if result else {}

    # === Queries ===

    def query_person_projects(self, person_name: str) -> List[Dict]:
        return self._run(
            """
            MATCH (p:Person {name: $name})-[:WORKED_ON]->(proj:Project)
            OPTIONAL MATCH (proj)-[:USES]->(tech:Technology)
            RETURN proj.name as project, collect(tech.name) as technologies
            """,
            name=person_name,
        )

    def query_person_skills(self, person_name: str) -> List[Dict]:
        return self._run(
            """
            MATCH (p:Person {name: $name})-[r:HAS_SKILL]->(s:Skill)
            RETURN s.name as skill, r.level as level
            ORDER BY r.level DESC
            """,
            name=person_name,
        )

    def query_related_people(self, skill_name: str) -> List[Dict]:
        return self._run(
            """
            MATCH (p:Person)-[r:HAS_SKILL]->(s:Skill {name: $skill})
            RETURN p.name as person, r.level as level
            ORDER BY r.level DESC
            """,
            skill=skill_name,
        )

    def count_nodes(self) -> Dict:
        result = self._run(
            "MATCH (n) RETURN labels(n) as label, count(n) as count"
        )
        return {
            r.get("label", ["Unknown"])[0]: r["count"] for r in result
        }

    def ping(self) -> bool:
        try:
            self._run("RETURN 1")
            return True
        except Exception:
            return False
