from fastapi import Depends, FastAPI, HTTPException

from schemas.cart import (
    CartDisplay,
    CartItemCreate,
    CartItemDisplay,
    CartItemRemoveRequest,
)
from schemas.item import ItemCreate, ItemDisplay, ItemUpdate

from typing import List

from infrastructure.repository import ItemRepository
from domain.repo_interfaces import IItemRepository, ICartRepository
from app.dependencies import get_item_repository, get_item_service, get_cart_repository, get_cart_service
from domain.service import ItemService,CartService

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World! If you can read this, the project is ready to use at http://0.0.0.0:8000/docs"}

@app.post("/item/", response_model=ItemDisplay)
def create_item(item_data: ItemCreate, item_service: ItemService = Depends(get_item_service)):
    created_item = item_service.create_item(item_data)
    return created_item


@app.get("/item/all", response_model=List[ItemDisplay])
def list_items(item_repo: ItemRepository = Depends(get_item_repository)):
    items = item_repo.list()
    return items


@app.get("/item/{item_id}", response_model=ItemDisplay)
def get_single_item(item_id: int, item_repo: IItemRepository = Depends(get_item_repository)):
    item = item_repo.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/item/{item_id}", response_model=ItemDisplay)
def update_item(item_id: int, item_update: ItemUpdate, item_service: ItemService = Depends(get_item_service)):
    updated_item = item_service.update_item(item_id=item_id, item_data=item_update)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@app.delete("/item/{item_id}", status_code=200)
def delete_item(item_id: int, item_repo: IItemRepository = Depends(get_item_repository)):
    try:
        item_repo.delete(item_id=item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "Item deleted successfully"}


@app.post("/cart/", response_model=CartDisplay)
def create_empty_cart(cart_repo: ICartRepository = Depends(get_cart_repository)):
    new_cart = cart_repo.create()
    return new_cart


@app.get("/cart/all", response_model=List[CartDisplay])
def list_all_carts(cart_service: CartService = Depends(get_cart_service)):
    return cart_service.list_carts_with_details()


@app.get("/cart/{cart_id}", response_model=CartDisplay)
def read_cart(cart_id: int, cart_service: CartService = Depends(get_cart_service)):
    return cart_service.get_cart_details(cart_id)


@app.get("/cart/{cart_id}", response_model=CartDisplay)
def read_cart(cart_id: int, cart_service: CartService = Depends(get_cart_service)):
    return cart_service.get_cart_details(cart_id)

@app.post("/cart/{cart_id}/add", response_model=CartItemDisplay)
def add_item_to_cart(
    cart_id: int, cart_item: CartItemCreate, cart_service: CartService = Depends(get_cart_service)
):
    return cart_service.add_item_to_cart(cart_id, cart_item.item_id, cart_item.quantity)


@app.delete("/cart/{cart_id}/remove", status_code=200)
def remove_item_from_cart(
    cart_id: int, remove_request: CartItemRemoveRequest, cart_service: CartService = Depends(get_cart_service)
):
    cart_service.remove_item_from_cart(cart_id, remove_request.item_id, remove_request.quantity)
    return {"message": "Item(s) removed successfully"}
