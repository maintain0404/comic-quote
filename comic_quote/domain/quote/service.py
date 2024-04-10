from __future__ import annotations

from pydantic import BaseModel


class ComicQuote(BaseModel):
    content: str
    comic_name: str
    place: str
    author: str
    image: str | None


class RandomComicQuoteService:
    def get_random_quote(self) -> ComicQuote:
        ...
