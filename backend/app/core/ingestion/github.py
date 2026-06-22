"""GitHub repository analyzer — extracts project info for digital twin knowledge."""
import re
import logging
from typing import Optional, Dict, List
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

GITHUB_URL_PATTERN = re.compile(r"github\.com/([^/]+)/([^/\s#?]+)")


def parse_github_url(url: str) -> Optional[tuple[str, str]]:
    """Extract owner/repo from GitHub URL. Returns (owner, repo) or None."""
    # Handle various formats
    url = url.strip().rstrip("/").rstrip(".git")
    match = GITHUB_URL_PATTERN.search(url)
    if match:
        return match.group(1), match.group(2)
    # Try simple path parsing
    parsed = urlparse(url)
    if "github.com" in parsed.netloc:
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) >= 2:
            return parts[0], parts[1]
    return None


class GitHubRepoAnalyzer:
    """Analyzes GitHub repos to extract project knowledge."""

    @staticmethod
    async def fetch_readme(owner: str, repo: str) -> Optional[str]:
        """Try fetching README from GitHub raw content."""
        import aiohttp
        urls = [
            f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md",
            f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md",
            f"https://raw.githubusercontent.com/{owner}/{repo}/main/README",
            f"https://raw.githubusercontent.com/{owner}/{repo}/master/README",
            f"https://raw.githubusercontent.com/{owner}/{repo}/main/readme.md",
            f"https://raw.githubusercontent.com/{owner}/{repo}/master/readme.md",
        ]
        for url in urls:
            try:
                async with aiohttp.ClientSession(trust_env=False) as session:
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                        if resp.status == 200:
                            return await resp.text()
            except Exception:
                continue
        return None

    @staticmethod
    async def fetch_file(owner: str, repo: str, path: str) -> Optional[str]:
        """Fetch a specific file from the repo."""
        import aiohttp
        urls = [
            f"https://raw.githubusercontent.com/{owner}/{repo}/main/{path}",
            f"https://raw.githubusercontent.com/{owner}/{repo}/master/{path}",
        ]
        for url in urls:
            try:
                async with aiohttp.ClientSession(trust_env=False) as session:
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                        if resp.status == 200:
                            return await resp.text()
            except Exception:
                continue
        return None

    @staticmethod
    async def analyze(owner: str, repo: str) -> Dict:
        """Analyze a GitHub repo and return structured project info."""
        result = {
            "owner": owner,
            "repo": repo,
            "url": f"https://github.com/{owner}/{repo}",
            "readme": None,
            "package_json": None,
            "pyproject_toml": None,
            "requirements_txt": None,
            "tech_stack": [],
            "summary": "",
        }

        # Fetch README
        readme = await GitHubRepoAnalyzer.fetch_readme(owner, repo)
        if readme:
            result["readme"] = readme[:10000]

        # Fetch dependency files
        pkg = await GitHubRepoAnalyzer.fetch_file(owner, repo, "package.json")
        if pkg:
            result["package_json"] = pkg
            try:
                import json
                data = json.loads(pkg)
                deps = {}
                deps.update(data.get("dependencies", {}))
                deps.update(data.get("devDependencies", {}))
                result["tech_stack"].extend(list(deps.keys()))
            except Exception:
                pass

        pyproject = await GitHubRepoAnalyzer.fetch_file(owner, repo, "pyproject.toml")
        if pyproject:
            result["pyproject_toml"] = pyproject[:5000]

        reqs = await GitHubRepoAnalyzer.fetch_file(owner, repo, "requirements.txt")
        if reqs:
            result["requirements_txt"] = reqs[:5000]
            for line in reqs.split("\n"):
                line = line.strip()
                if line and not line.startswith("#"):
                    pkg_name = line.split("=")[0].split(">")[0].split("<")[0].strip()
                    if pkg_name and len(pkg_name) > 1:
                        result["tech_stack"].append(pkg_name)

        # Deduplicate tech stack
        result["tech_stack"] = sorted(set(
            t.replace("@", "").split("/")[-1] for t in result["tech_stack"]
        ))[:30]

        return result

    @staticmethod
    def extract_knowledge(repo_data: Dict, project_url: str) -> str:
        """Convert repo analysis into natural language knowledge for RAG."""
        parts = [f"Project: {repo_data['repo']}"]
        parts.append(f"GitHub: {repo_data['url']}")

        if repo_data["readme"]:
            parts.append(f"README: {repo_data['readme'][:2000]}")

        if repo_data["tech_stack"]:
            parts.append(f"Technologies: {', '.join(repo_data['tech_stack'])}")

        return "\n\n".join(parts)
