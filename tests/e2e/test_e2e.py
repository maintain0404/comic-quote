from __future__ import annotations

import pytest
from litestar.testing import AsyncTestClient


@pytest.fixture()
async def client():
    from comic_quote.app import app

    return AsyncTestClient(app)


async def test_random_quote_api_success(client: AsyncTestClient):
    async with client:
        resp = await client.get("api/0.1.0/quotes/random")
        assert resp.status_code == 200

        data = resp.json()

        assert "content" in data
        assert "artwork_name" in data
        assert "location" in data
