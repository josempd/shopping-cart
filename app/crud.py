from sqlalchemy.orm import Session

from . import models
from .schemas import ItemCreate


def create_item(db: Session, item: ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_cart(db: Session):
    db_cart = models.Cart()
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


def get_cart(db: Session, cart_id: int):
    return db.query(models.Cart).filter(models.Cart.id == cart_id).first()


def delete_cart(db: Session, cart_id: int):
    db_cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if db_cart:
        db.delete(db_cart)
        db.commit()
        return True
    return False


def get_carts(db: Session):
    return db.query(models.Cart).all()
