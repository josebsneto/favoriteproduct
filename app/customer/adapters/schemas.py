from dataclasses import dataclass

from pydantic import BaseModel

from app import settings


class PaginatorResponse(BaseModel):
    page: int
    size: int = settings.PAGE_SIZE
    total: int


@dataclass
class Paginator:
    def __init__(self, page: int = 1, limit: int | None = None):
        self.limit = limit or settings.PAGE_SIZE
        self.page = page if page > 0 else 1

    def make_paginator(self):
        skip = self.limit * (self.page - 1)
        return skip, self.limit
