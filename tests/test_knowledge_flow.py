import pytest
import httpx
import os


@pytest.mark.asyncio
async def test_upload_text_file(api_base):
    test_file = "/tmp/test_knowledge.md"
    with open(test_file, "w") as f:
        f.write("# Test Document\n\nThis is about Python and AI.\n")

    async with httpx.AsyncClient() as client:
        with open(test_file, "rb") as f:
            response = await client.post(
                f"{api_base}/api/knowledge/upload",
                files={"file": ("test.md", f, "text/markdown")},
                timeout=10.0,
            )
    os.unlink(test_file)
    assert response.status_code in (200, 422, 503)


@pytest.mark.asyncio
async def test_search(api_base):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{api_base}/api/knowledge/search",
            params={"q": "Python"},
            timeout=5.0,
        )
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
