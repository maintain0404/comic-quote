from __future__ import annotations

from comic_quote.domain.quote.repo import QuoteRepo
from litestar import get
from litestar.di import Provide
from litestar.response import Template

from ..domain.quote.impl import QuoteImpl

_SERVICE = QuoteImpl(repo=QuoteRepo())


@get(
    path="/", dependencies={"service": Provide(lambda: _SERVICE, sync_to_thread=False)}
)
async def index(service: QuoteImpl) -> Template:
    model = await service.get_random_quote()
    return Template(template_name="index.html.j2", context={"quote": model})
