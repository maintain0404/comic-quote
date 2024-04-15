from __future__ import annotations

from comic_quote.domain.quote.entity import Quote
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository


class QuoteRepo(SQLAlchemyAsyncRepository[Quote]):
    model_type = Quote
