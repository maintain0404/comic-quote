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
from litestar.logging.config import StructLoggingConfig
from litestar.plugins.structlog import StructlogConfig, StructlogPlugin
from litestar.template.config import TemplateConfig

from .config import Config
from .config import config as global_config
from .handler.htmx import QuoteHTMXController
from .handler.rest import QuoteAPIController, healthcheck
from .vendor.app import Application

__all__ = ["all"]


def create_app(config: Config):
    sqla_plugin = SQLAlchemyInitPlugin(
        config=SQLAlchemyAsyncConfig(
            connection_string=config.sa_uri,
            session_config=AsyncSessionConfig(expire_on_commit=True),
            alembic_config=AlembicAsyncConfig(
                script_location="comic_quote/core/db/migrations"
            ),
        ),
    )
    return Application(
        route_handlers=[
            QuoteHTMXController,
            Router("api/0.1.0/", route_handlers=[QuoteAPIController, healthcheck]),
            # create_static_files_router(path="/static", directories=["assets"]),
        ],
        template_config=TemplateConfig(
            directory=Path("jinja2"),
            engine=JinjaTemplateEngine,
        ),
        plugins=[
            sqla_plugin,
            StructlogPlugin(
                config=StructlogConfig(
                    structlog_logging_config=StructLoggingConfig(
                        log_exceptions="always"
                    )
                )
            ),
        ],
    )


app = create_app(global_config)
