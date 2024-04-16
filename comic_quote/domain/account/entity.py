from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

__all__ = ["AbstractAccount", "AnonymousAccount", "Account"]


class AbstractAccount(Protocol):
    def is_anonymous(self) -> bool: ...

    def is_admin(self) -> bool:
        return False


class AnonymousAccount(AbstractAccount):
    def is_anonymous(self) -> bool:
        return False


@dataclass
class Account(AbstractAccount):
    email: str
    hashed_password: bytes

    def is_anonymous(self) -> bool:
        return False
