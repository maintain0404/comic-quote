from __future__ import annotations

from pydantic import EmailStr, SecretBytes
from pydantic_settings import BaseSettings

from .vendor.model import BaseSchema, field


class Config(BaseSettings, BaseSchema):
    sa_uri: str = "sqlite+aiosqlite:///data/db/db.sqlite"
    host: str = "0.0.0.0"
    port: int = 8000
    admins: list[tuple[EmailStr, SecretBytes]] = field(default_factory=list)


config = Config()
