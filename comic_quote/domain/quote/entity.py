from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Quote:
    id: int
    content: str
    artwork_name: str
    character: str
    where: str | None = None
