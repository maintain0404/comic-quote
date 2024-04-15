from __future__ import annotations

from litestar import Controller, get
from litestar.response import Template

from ..domain.quote.impl import QuoteImpl
from .deps import DEPENDENCIES


class QuoteHTMXController(Controller):
    path = "/quotes"
    dependencies = DEPENDENCIES

    @get("/")
    async def get_a_random_quote(self, service: QuoteImpl) -> Template:
        model = await service.get_random_quote()
        return Template(template_name="index.html.j2", context={"quote": model})
