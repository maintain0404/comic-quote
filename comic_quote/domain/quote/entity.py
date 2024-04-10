from __future__ import annotations

from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, mapped_column


class ComicQuote(DeclarativeBase):
    id: Annotated[int, mapped_column(primary_key=True)]
    content: str
    comic_name: str
    place: str
    author: str
    image: str | None
