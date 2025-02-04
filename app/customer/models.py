from pydantic import BaseModel, Field


class Customer(BaseModel):
    email: str
    name: str
    product_ids: list[str] = Field(default_factory=list)

    def add_product(self, product_id: str) -> None:
        if product_id not in self.product_ids:
            self.product_ids.insert(0, product_id)

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Customer) and self.email == other.email
