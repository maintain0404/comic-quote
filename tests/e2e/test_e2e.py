from __future__ import annotations

from typing import cast

import pytest
from comic_quote.app import create_app
from comic_quote.config import Config
from comic_quote.domain.quote import Quote, QuoteRepo
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyInitPlugin
from litestar.testing import AsyncTestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


@pytest.fixture()
async def app():
    config = Config(sa_uri="sqlite+aiosqlite:///data/db/test.sqlite")
    from advanced_alchemy.base import orm_registry

    app = create_app(config)
    plugin: SQLAlchemyInitPlugin = app.plugins.get("SQLAlchemyInitPlugin")
    engine: AsyncEngine = plugin._config.get_engine()

    async def prepare():
        async with engine.connect() as conn:
            async with conn.begin():
                await conn.run_sync(lambda c: orm_registry.metadata.create_all(c))

            await conn.commit()

    await prepare()

    yield app

    async def drop():
        import os

        os.remove("data/db/test.sqlite")

    await drop()


@pytest.fixture()
async def client(app):
    return AsyncTestClient(app)


@pytest.fixture()
async def db_session(app):
    plugin: SQLAlchemyInitPlugin = app.plugins.get("SQLAlchemyInitPlugin")

    async with cast(AsyncSession, plugin._config.get_session()) as session:
        yield session


async def test_healthcheck(client: AsyncTestClient):
    async with client:
        resp = await client.get("api/0.1.0/health")
        data = resp.json()
        assert data["status"] == "ok"
        assert resp.status_code == 200


async def test_random_quote_api_success(
    client: AsyncTestClient, db_session: AsyncSession
):
    repo = QuoteRepo(session=db_session)

    async with db_session.begin():
        await repo.add_many(
            [
                Quote(
                    content="...아무 일!!! 없었다!!!",
                    artwork_name="원피스",
                    character="롤로노아 조로",
                ),
                Quote(
                    content="계획대로",
                    artwork_name="데스노트",
                    character="야가미 라이토",
                ),
            ]
        )

    db_session.expunge_all()

    # Try 10 times to test random
    for _ in range(10):
        async with client:
            resp = await client.get("api/0.1.0/quotes/random")
            data = resp.json()
            if data["artwork_name"] == "원피스":
                assert data["content"] == "...아무 일!!! 없었다!!!"
                assert data["character"] == "롤로노아 조로"
            elif data["artwork_name"] == "데스노트":
                assert data["content"] == "계획대로"
                assert data["character"] == "야가미 라이토"
            assert resp.status_code == 200


async def test_admin_api_quote_create_success(
    client: AsyncTestClient, db_session: AsyncSession
):
    async with client:
        resp = await client.post(
            "/admin/quotes",
            json=dict(
                content="...아무 일!!! 없었다!!!",
                artwork_name="원피스",
                character="롤로노아 조로",
            ),
        )
        # for checking response with pytest -l option
        data = resp.json()  # noqa: F841
        assert resp.status_code == 201

    async with db_session.begin():
        assert (
            len(
                list(
                    await db_session.scalars(
                        select(Quote).where(
                            Quote.artwork_name == "원피스",
                            Quote.character == "롤로노아 조로",
                        )
                    )
                )
            )
            == 1
        )


async def test_admin_api_quote_delete_success(
    client: AsyncTestClient, db_session: AsyncSession
):
    repo = QuoteRepo(session=db_session)

    async with db_session.begin():
        quote = await repo.add(
            Quote(
                content="...아무 일!!! 없었다!!!",
                artwork_name="원피스",
                character="롤로노아 조로",
            )
        )

    db_session.expunge_all()

    async with client:
        resp = await client.delete(
            f"/admin/quotes/{quote.id}",
        )
        # for checking response with pytest -l option
        data = resp.json()  # noqa: F841
        assert resp.status_code == 200

    async with db_session.begin():
        assert (
            len(
                await repo.list(
                    Quote.artwork_name == "원피스", Quote.character == "롤로노아 조로"
                )
            )
            == 0
        )


async def test_admin_api_quote_update_success(
    client: AsyncTestClient, db_session: AsyncSession
):
    repo = QuoteRepo(session=db_session)

    async with db_session.begin():
        quote = await repo.add(
            Quote(
                content="...아무 일!!! 없었다!!!",
                artwork_name="원피스",
                character="롤로노아 조로",
            )
        )

    db_session.expunge_all()

    async with client:
        resp = await client.put(
            f"/admin/quotes/{quote.id}",
            json=dict(
                content="...아무 일!!! 있었다!!!",
                artwork_name="원피스",
                character="롤로노아 조로",
            ),
        )
        # for checking response with pytest -l option
        data = resp.json()  # noqa: F841
        assert resp.status_code == 200

    async with db_session.begin():
        obj = await db_session.scalar(select(Quote).where(Quote.id == quote.id))

    assert obj.content == "...아무 일!!! 있었다!!!"
    assert obj.artwork_name == "원피스"
    assert obj.character == "롤로노아 조로"
