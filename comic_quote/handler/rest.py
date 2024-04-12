from __future__ import annotations

from comic_quote.domain.quote.repo import QuoteRepo
from litestar import Controller, get
from litestar.contrib.pydantic import PydanticDTO
from litestar.dto import DTOConfig

from ..domain.quote.impl import QuoteImpl
from ..vendor.model import BaseSchema


class DTO(PydanticDTO):
    config = DTOConfig()


class QuoteSchema(BaseSchema):
    content: str
    artwork_name: str
    character: str
    location: str | None


class QuoteAPIController(Controller):
    path = "/quotes"
    dto = DTO
    service = QuoteImpl(QuoteRepo())

    @get("/random")
    async def get_a_random_quote(self) -> QuoteSchema:
        model = await self.service.get_random_quote()
        return QuoteSchema.model_validate(model)
