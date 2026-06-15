import pytest
import httpx


@pytest.mark.asyncio
async def test_pending_facts_endpoint(api_base):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{api_base}/api/evolution/pending",
            timeout=5.0,
        )
    assert response.status_code == 200
    data = response.json()
    assert "facts" in data
