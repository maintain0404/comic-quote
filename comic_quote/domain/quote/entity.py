from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Quote:
    id: int
    content: str
    artwork_name: str
    character: str
    location: str | None = None
