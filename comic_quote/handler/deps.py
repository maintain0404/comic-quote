from __future__ import annotations

from comic_quote.domain.account.impl import AccountImpl
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import config
from ..domain.quote import QuoteImpl

_ACCOUNT_IMPL = AccountImpl.from_email_and_passwords(config.admins)


async def quote_impl(db_session: AsyncSession):
    async with db_session.begin():
        yield QuoteImpl(session=db_session)


def account_impl() -> AccountImpl:
    return _ACCOUNT_IMPL


DEPENDENCIES = {
    "service": Provide(quote_impl),
    "account_svc": Provide(account_impl, sync_to_thread=False),
}
