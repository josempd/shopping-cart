from pydantic import BaseModel


# For creating a new item
class ItemCreate(BaseModel):
    name: str
    price: float
    description: str
    thumbnail: str
    stock: int
    type: str


class ItemDisplay(BaseModel):
    id: int
    name: str
    price: float
    description: str
    thumbnail: str
    stock: int
    type: str

    class Config:
        orm_mode = True


class CartItemCreate(BaseModel):
    item_id: int
    quantity: int


class CartItemDisplay(BaseModel):
    item_id: int
    quantity: int
    item: ItemDisplay

    class Config:
        orm_mode = True


class CartDisplay(BaseModel):
    id: int
    items: list[CartItemDisplay] = []

    class Config:
        orm_mode = True
