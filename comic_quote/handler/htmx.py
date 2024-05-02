from __future__ import annotations

from litestar import Controller, delete, get, post, put
from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar.contrib.pydantic import PydanticDTO
from pydantic import BaseModel

from ..config import config
from ..domain.quote.impl import QuoteImpl
from .deps import DEPENDENCIES

__all__ = ["QuoteHTMXController", "AdminController"]


class QuoteHTMXController(Controller):
    path = "/quotes"
    dependencies = DEPENDENCIES

    @get("/")
    async def get_a_random_quote(self, service: QuoteImpl) -> HTMXTemplate:
        model = await service.get_random_quote()
        return HTMXTemplate(template_name="index.html.j2", context={"quote": model})


class _Quote(BaseModel):
    content: str
    artwork_name: str
    character: str
    location: str | None


class CreateQuote(_Quote): ...


class UpdateQuote(_Quote): ...


class AdminController(Controller):
    path = config.admin_page_url
    dependencies = DEPENDENCIES
    request_class = HTMXRequest

    @get("/login")
    async def admin_login_page(self) -> HTMXTemplate:
        return HTMXTemplate(template_name="admin.html.j2")

    @post("/login")
    async def admin_login(self) -> HTMXTemplate: ...

    @get("/")
    async def admin_page(self, service: QuoteImpl) -> HTMXTemplate:
        return HTMXTemplate(
            template_name="admin.html.j2", context={"quotes": await service.list()}
        )

    @post("/quotes", dto=PydanticDTO[CreateQuote])
    async def add_quote(self, data: CreateQuote, service: QuoteImpl) -> None:
        await service.create(data.model_dump(), auto_refresh=False)

    @put("/quotes/{id:int}", dto=PydanticDTO[UpdateQuote], status_code=200)
    async def update_quote(
        self, id: int, data: UpdateQuote, service: QuoteImpl
    ) -> None:
        await service.update(data=data.model_dump(), item_id=id)

    # HTMX do not fire event on 204(litesar delete default)
    @delete("/quotes/{id:int}", status_code=200)
    async def delete_quote(self, id: int, service: QuoteImpl) -> None:
        await service.delete(id)
