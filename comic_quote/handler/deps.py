from __future__ import annotations

from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession

from ..domain.quote import QuoteImpl, QuoteRepo


async def quote_impl(db_session: AsyncSession) -> QuoteImpl:
    return QuoteImpl(repo=QuoteRepo(session=db_session))


DEPENDENCIES = {
    "service": Provide(quote_impl),
}
