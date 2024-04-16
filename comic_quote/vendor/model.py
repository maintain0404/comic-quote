from __future__ import annotations

from pydantic import BaseModel as BaseModel_
from pydantic import ConfigDict
from pydantic import Field as field

__all__ = ["BaseSchema", "ConfigDict", "field"]


class BaseSchema(BaseModel_):
    model_config = ConfigDict(extra="ignore", from_attributes=True)
