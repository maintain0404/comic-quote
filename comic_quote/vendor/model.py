from __future__ import annotations

from pydantic import BaseModel as BaseModel_
from pydantic import ConfigDict


class BaseSchema(BaseModel_):
    model_config = ConfigDict(extra="ignore", from_attributes=True)
