from __future__ import annotations

from dataclasses import dataclass

import bcrypt
from comic_quote.domain.account.entity import Account
from litestar.exceptions import NotAuthorizedException


@dataclass
class AccountImpl:
    accounts: dict[str, Account]

    async def login(self, email: str, password: str) -> Account:
        account = self.accounts.get(email, None)
        if not account:
            raise NotAuthorizedException

        if bcrypt.checkpw(password.encode(), account.hashed_password):
            return account
        else:
            raise NotAuthorizedException

    async def authenticate(self, email: str) -> Account:
        account = self.accounts.get(email, None)
        if not account:
            raise NotAuthorizedException
        return account
