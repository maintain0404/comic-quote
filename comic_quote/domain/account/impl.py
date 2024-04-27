from __future__ import annotations

from dataclasses import dataclass
from typing import Self

import bcrypt
from comic_quote.domain.account.entity import Account
from litestar.exceptions import NotAuthorizedException


@dataclass
class AccountImpl:
    accounts: dict[str, Account]

    @classmethod
    def from_email_and_passwords(cls, email_and_pws: list[str, str]) -> Self:
        accounts = {}
        for email, origin_pw in email_and_pws:
            hashed_pw = bcrypt.hashpw(origin_pw.encode(), bcrypt.gensalt())
            accounts[email] = Account(email=email, hashed_password=hashed_pw)

        return cls(accounts)

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
