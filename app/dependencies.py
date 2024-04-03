from fastapi import Depends
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from infrastructure.repository import ItemRepository, CartRepository
from domain.repo_interfaces import ICartRepository
from domain.service import ItemService, CartService

def get_item_repository(db: Session = Depends(get_db)):
    return ItemRepository(db)

def get_item_service(db: Session = Depends(get_db)) -> ItemService:
    item_repo = ItemRepository(db)
    return ItemService(item_repo)

def get_cart_repository(db: Session = Depends(get_db)) -> ICartRepository:
    return CartRepository(db)

def get_cart_service(db: Session = Depends(get_db)) -> CartService:
    cart_repository = CartRepository(db)
    item_repository = ItemRepository(db)
    return CartService(cart_repository, item_repository)
