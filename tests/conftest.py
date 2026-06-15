import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def api_base():
    return os.getenv("API_BASE_URL", "http://localhost:8000")


@pytest.fixture
def test_text():
    return "This is a test document about Python programming and AI development."
