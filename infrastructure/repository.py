from sqlalchemy.orm import Session
from domain.models import Item, Cart, CartItem
from domain.repo_interfaces import IItemRepository, ICartRepository
from domain.models import Base
from typing import List, Optional

from domain.service import CartService
from fastapi import HTTPException

class ItemRepository(IItemRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, item: Item) -> Item:
        self.db_session.add(item)
        self.db_session.commit()
        return item

    def get(self, item_id: int) -> Optional[Item]:
        return self.db_session.query(Item).filter(Item.id == item_id).one_or_none()

    def list(self) -> List[Item]:
        return self.db_session.query(Item).all()

    def update(self, item_id: int, item_data: dict) -> Optional[Item]:
        item = self.db_session.query(Item).filter(Item.id == item_id).one_or_none()
        if item:
            for key, value in item_data.items():
                setattr(item, key, value)
            self.db_session.commit()
            return item
        return None

    def delete(self, item_id: int) -> None:
        item_to_delete = self.db_session.query(Item).filter(Item.id == item_id).one_or_none()
        if item_to_delete:
            self.db_session.delete(item_to_delete)
            self.db_session.commit()
        else:
            raise ValueError("Item not found")


    def delete(self, item_id: int) -> None:
        item_to_delete = self.db_session.query(Item).filter(Item.id == item_id).one_or_none()
        if item_to_delete:
            self.db_session.delete(item_to_delete)
            self.db_session.commit()
        else:
            raise ValueError("Item not found")

class CartRepository(ICartRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self) -> Cart:
        new_cart = Cart()
        self.db_session.add(new_cart)
        self.db_session.commit()
        return new_cart

    def get(self, cart_id: int) -> Optional[Cart]:
        return self.db_session.query(Cart).filter(Cart.id == cart_id).one_or_none()

    def list(self) -> List[Cart]:
        return self.db_session.query(Cart).all()

    def delete(self, cart_id: int) -> None:
        cart_to_delete = self.db_session.query(Cart).filter(Cart.id == cart_id).one_or_none()
        if cart_to_delete:
            self.db_session.delete(cart_to_delete)
            self.db_session.commit()
        else:
            raise ValueError("Cart not found")

    def get_cart_item(self, cart_id: int, item_id: int) -> Optional[CartItem]:
        return self.db_session.query(CartItem).filter_by(cart_id=cart_id, item_id=item_id).first()

    def add_cart_item(self, cart_item: CartItem) -> None:
        self.db_session.add(cart_item)
        self.db_session.commit()

    def remove_cart_item(self, cart_item: CartItem) -> None:
        self.db_session.delete(cart_item)
        self.db_session.commit()

    def update_cart_item(self, cart_id: int, item_id: int, changes: dict) -> Optional[CartItem]:
        """Update a cart item with the given changes and commit the transaction."""
        cart_item = self.db_session.query(CartItem).filter_by(cart_id=cart_id, item_id=item_id).first()
        if cart_item:
            for key, value in changes.items():
                setattr(cart_item, key, value)
            self.db_session.commit()
            return cart_item
        return None
