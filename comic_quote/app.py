from __future__ import annotations

from pathlib import Path

from advanced_alchemy import AlembicAsyncConfig
from litestar import Router
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.contrib.sqlalchemy.plugins import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig

from .config import config
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
    plugins=[
        SQLAlchemyInitPlugin(
            config=SQLAlchemyAsyncConfig(
                connection_string=config.sa_uri,
                session_config=AsyncSessionConfig(expire_on_commit=True),
                alembic_config=AlembicAsyncConfig(
                    script_location="comic_quote/core/db/migrations"
                ),
            ),
        ),
    ],
)
