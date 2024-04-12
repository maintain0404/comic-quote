from __future__ import annotations

from pathlib import Path

from litestar import Router
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig

from .handler.htmx import QuoteHTMXController
from .handler.rest import QuoteAPIController
from .vendor.app import Application

app = Application(
    route_handlers=[
        QuoteHTMXController,
        Router("api/0.1.0/", route_handlers=[QuoteAPIController]),
        create_static_files_router(path="/static", directories=["assets"]),
    ],
    template_config=TemplateConfig(
        directory=Path("jinja2"),
        engine=JinjaTemplateEngine,
    ),
)
