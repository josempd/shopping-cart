from pydantic import BaseModel, Field


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


class ItemUpdate(BaseModel):
    name: str | None = Field(None, description="The name of the item")
    price: float | None = Field(None, description="The price of the item")
    description: str | None = Field(None, description="A description of the item")
    thumbnail: str | None = Field(None, description="URL to an image of the item")
    stock: int | None = Field(None, description="How many of these items are in stock")
    type: str | None = Field(
        None, description="The type of the item (Product or Event)"
    )


class CartItemRemoveRequest(BaseModel):
    item_id: int = Field(..., description="The ID of the item to remove from the cart")
    quantity: int | None = Field(
        None, gt=0, description="The quantity of the item to remove"
    )


class ItemDeleteRequest(BaseModel):
    item_ids: int | list[int] = Field(
        ..., description="A single item ID or a list of item IDs to delete"
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
        orm_mode = True


class CartDisplay(BaseModel):
    id: int
    items: list[CartItemDisplay] = []
    total: float = Field(0, description="The total price of all items in the cart")

    class Config:
        orm_mode = True
