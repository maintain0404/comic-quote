from __future__ import annotations

from litestar.contrib.sqlalchemy.base import BigIntBase
from sqlalchemy.orm import Mapped


class Quote(BigIntBase):
    content: Mapped[str]
    artwork_name: Mapped[str]
    character: Mapped[str]
    location: Mapped[str | None] = None
