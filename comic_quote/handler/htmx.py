from __future__ import annotations

from comic_quote.domain.quote.repo import QuoteRepo
from litestar import Controller, get
from litestar.response import Template

from ..domain.quote.impl import QuoteImpl


class QuoteHTMXController(Controller):
    path = "/quotes"
    service = QuoteImpl(QuoteRepo())

    @get("/")
    async def get_a_random_quote(self) -> Template:
        model = await self.service.get_random_quote()
        return Template(template_name="index.html.j2", context={"quote": model})
