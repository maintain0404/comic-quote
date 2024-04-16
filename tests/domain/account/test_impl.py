from __future__ import annotations

import bcrypt
import pytest
from comic_quote.domain.account.entity import Account
from comic_quote.domain.account.impl import AccountImpl
from litestar.exceptions import NotAuthorizedException


async def test_login_success():
    impl = AccountImpl(
        {
            "test@test.com": Account(
                "test@test.com", bcrypt.hashpw(b"pw123", bcrypt.gensalt())
            ),
        },
    )

    account = await impl.login("test@test.com", "pw123")

    assert account.email == "test@test.com"


async def test_login_with_user_not_exists():
    impl = AccountImpl(
        {
            "test@test.com": Account(
                "test@test.com", bcrypt.hashpw(b"pw123", bcrypt.gensalt())
            ),
        },
    )

    with pytest.raises(NotAuthorizedException):
        await impl.login("nouser@test.com", "pw123")


async def test_login_with_user_invalid_password():
    impl = AccountImpl(
        {
            "test@test.com": Account(
                "test@test.com", bcrypt.hashpw(b"pw123", bcrypt.gensalt())
            ),
        },
    )

    with pytest.raises(NotAuthorizedException):
        await impl.login("nouser@test.com", "pw1")
