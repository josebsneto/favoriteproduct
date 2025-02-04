from typing import Any

from pydantic import BaseModel

from app.customer.adapters.schemas import PaginatorResponse
from app.customer.models import Customer


class CustomerCreate(BaseModel):
    email: str
    name: str


class CustomerUpdate(BaseModel):
    name: str


class ProductCreate(BaseModel):
    product_id: str


class CustomerGetResponse(BaseModel):
    item: Customer
    paginator_product_ids: PaginatorResponse


class ProductGetResponse(BaseModel):
    items: list[dict[Any, Any]]
    paginator: PaginatorResponse
