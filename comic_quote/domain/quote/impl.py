from __future__ import annotations

import random
from dataclasses import dataclass

from comic_quote.domain.quote.repo import QuoteRepo


@dataclass
class QuoteModel:
    content: str
    artwork_name: str
    character: str
    location: str | None


@dataclass
class QuoteImpl:
    repo: QuoteRepo

    async def get_random_quote(self) -> QuoteModel:
        cnt = await self.repo.count()
        id = random.randint(1, cnt)
        entity = await self.repo.get_one_or_none(id)

        return QuoteModel(
            content=entity.content,
            artwork_name=entity.artwork_name,
            character=entity.character,
            location=entity.location,
        )
