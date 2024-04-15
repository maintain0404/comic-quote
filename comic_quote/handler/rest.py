from __future__ import annotations

from litestar import Controller, get
from litestar.contrib.pydantic import PydanticDTO
from litestar.dto import DTOConfig

from ..domain.quote.impl import QuoteImpl
from ..vendor.model import BaseSchema
from .deps import DEPENDENCIES


class DTO(PydanticDTO):
    config = DTOConfig()


class QuoteSchema(BaseSchema):
    content: str
    artwork_name: str
    character: str
    location: str | None


class QuoteAPIController(Controller):
    path = "/quotes"
    dependencies = DEPENDENCIES

    @get("/random", dto=DTO[QuoteSchema])
    async def get_a_random_quote(self, service: QuoteImpl) -> QuoteSchema:
        model = await service.get_random_quote()
        return QuoteSchema.model_validate(model)
