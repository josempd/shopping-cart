from pydantic import BaseModel, Field, constr
from typing import Optional, Union, List

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
        from_attributes = True


class ItemUpdate(BaseModel):
    name: Optional[constr(min_length=1)] = Field(default=None, description="The name of the item")
    price: Optional[float] = Field(default=None, description="The price of the item")
    description: Optional[constr(min_length=1)] = Field(default=None, description="A description of the item")
    thumbnail: Optional[constr(min_length=1)] = Field(default=None, description="URL to an image of the item")
    stock: Optional[int] = Field(default=None, description="How many of these items are in stock")
    type: Optional[constr(min_length=1)] = Field(default=None, description="The type of the item (Product or Event)")

    class Config:
        min_anystr_length = 1
        anystr_strip_whitespace = True

class ItemDeleteRequest(BaseModel):
    item_ids: Union[int, List[int]] = Field(
        ..., description="A single item ID or a list of item IDs to delete"
    )
