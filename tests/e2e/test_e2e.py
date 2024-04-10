from __future__ import annotations

import pytest
from async_asgi_testclient import TestClient


@pytest.fixture(scope='session')
async def client():
    from comic_quote.app import app
    return TestClient(app)


async def test_random_quote_api_success(client: TestClient):
    async with client:
        resp = await client.get('')
        assert resp.status_code == 200
        
        data = resp.json()

        assert 'content' in data
        assert 'author' in data
        assert 'comic_name' in data
        assert 'place' in data


async def test_random_quote_page_success(client: TestClient):
    async with client:
        resp = await client.get('')
        assert resp.status_code == 200
        
        data = resp.json()

        assert 'content' in data
        assert 'author' in data
        assert 'comic_name' in data
        assert 'place' in data
