from __future__ import annotations

import random
from dataclasses import dataclass

from advanced_alchemy import SQLAlchemyAsyncRepositoryService

from .entity import Quote
from .repo import QuoteRepo


@dataclass
class QuoteModel:
    content: str
    artwork_name: str
    character: str
    location: str | None


class QuoteImpl(SQLAlchemyAsyncRepositoryService[Quote]):
    repository_type = QuoteRepo
    repository: QuoteRepo

    # TODO: Optimize
    async def get_random_quote(self) -> QuoteModel:
        cnt = await self.repository.count()
        id = random.randint(1, cnt)
        entity = await self.repository.get_one_or_none(id=id)

        return QuoteModel(
            content=entity.content,
            artwork_name=entity.artwork_name,
            character=entity.character,
            location=entity.location,
        )
