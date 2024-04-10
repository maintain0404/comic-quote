from __future__ import annotations

from pathlib import Path

from litestar import Router
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig

from .handler.htmx import index
from .handler.rest import ComicQuoteAPIController
from .vendor.app import Application

app = Application(
    route_handlers=[
        index,
        Router("api/0.1.0/", route_handlers=[ComicQuoteAPIController]),
        create_static_files_router(path="/static", directories=["assets"]),
    ],
    template_config=TemplateConfig(
        directory=Path("jinja2"),
        engine=JinjaTemplateEngine,
    ),
)
