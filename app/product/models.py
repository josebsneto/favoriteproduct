from pydantic import BaseModel


class Product(BaseModel):
    id: str
    title: str
    brand: str
    image_uri: str
    price: float
    reviewScore: float

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Product) and self.id == other.id
