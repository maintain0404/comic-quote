from __future__ import annotations

from comic_quote.domain.quote.repo import QuoteRepo
from litestar import Controller, get
from litestar.contrib.pydantic import PydanticDTO
from litestar.di import Provide
from litestar.dto import DTOConfig

from ..domain.quote.service import RandomComicQuoteService
from ..vendor.model import BaseModel

_SERVICE = RandomComicQuoteService(repo=QuoteRepo())


class DTO(PydanticDTO):
    config = DTOConfig()


class QuoteSchema(BaseModel):
    content: str
    artwork_name: str
    character: str
    where: str | None
    author: str
    image: str | None


class ComicQuoteAPIController(Controller):
    path = "/quotes"
    dependencies = {"service": Provide(lambda: _SERVICE, sync_to_thread=False)}

    @get("/random")
    async def get_a_random_quote(self, service: RandomComicQuoteService) -> QuoteSchema:
        model = await service.get_random_quote()
        schema = QuoteSchema(
            content=model.content,
            artwork_name=model.artwork_name,
            character=model.character,
            where=model.where,
            author=model.author,
            image=model.image,
        )
        return schema
