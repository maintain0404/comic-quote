from __future__ import annotations

from litestar import Router

from .handler.rest import ComicQuoteAPIController
from .vendor.app import Application

app = Application(
    route_handlers=[
        Router("api/0.1.0/", route_handlers=[ComicQuoteAPIController]),
    ]
)
