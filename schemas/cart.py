from pydantic import BaseModel, Field

from .item import ItemDisplay


class CartItemRemoveRequest(BaseModel):
    item_id: int = Field(..., description="The ID of the item to remove from the cart")
    quantity: int | None = Field(
        None, gt=0, description="The quantity of the item to remove"
    )


class CartCreate(BaseModel):
    pass


class CartItemCreate(BaseModel):
    item_id: int
    quantity: int


class CartItemDisplay(BaseModel):
    item_id: int
    quantity: int
    item: ItemDisplay
    subtotal: float = Field(
        0, description="The subtotal price for this item based on the quantity"
    )

    class Config:
        from_attributes = True


class CartDisplay(BaseModel):
    id: int
    items: list[CartItemDisplay] = []
    total: float = Field(0, description="The total price of all items in the cart")

    class Config:
        from_attributes = True
