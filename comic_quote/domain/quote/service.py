from __future__ import annotations

import random
from dataclasses import dataclass

from comic_quote.domain.quote.repo import QuoteRepo
from pydantic import BaseModel


class QuoteModel(BaseModel):
    content: str
    artwork_name: str
    who: str
    where: str | None
    author: str
    image: str | None


@dataclass
class RandomComicQuoteService:
    repo: QuoteRepo

    async def get_random_quote(self) -> QuoteModel:
        cnt = await self.repo.get_all_count()
        id = random.randint(1, cnt)
        entity = await self.repo.get_by_id(id)

        return QuoteModel(
            content=entity.content,
            artwork_name=entity.artwork_name,
            who=entity.who,
            where=entity.where,
            author=entity.author,
            image=entity.image,
        )
