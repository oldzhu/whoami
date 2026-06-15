import pytest
import httpx


@pytest.mark.asyncio
async def test_chat_endpoint_responds(api_base):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{api_base}/api/chat",
            json={"message": "Hello, who are you?"},
            timeout=10.0,
        )
    assert response.status_code in (200, 503)


@pytest.mark.asyncio
async def test_health_endpoint(api_base):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{api_base}/health", timeout=5.0)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_profile_endpoint(api_base):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{api_base}/api/profile", timeout=5.0)
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "skills" in data
