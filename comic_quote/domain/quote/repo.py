from __future__ import annotations


class ComicQuoteRepo:
    def get_all_count(self) -> int:
        ...

    def get_by_id(self, id: int) -> int:
        ...
