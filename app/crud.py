from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from schemas.cart import (
    CartDisplay,
    CartItemCreate,
    CartItemDisplay,
)
from schemas.item import ItemCreate, ItemDisplay, ItemUpdate

from . import models


def create_item(db: Session, item: ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(db: Session):
    return db.query(models.Item).all()


def update_item(db: Session, item_id: int, updated_item: ItemUpdate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        return None

    item_data = updated_item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_items(db: Session, item_ids: int | list[int]):
    if isinstance(item_ids, int):
        item_ids = [item_ids]  # Ensure item_ids is always a list
    db.query(models.Item).filter(models.Item.id.in_(item_ids)).delete(
        synchronize_session="fetch"
    )
    db.commit()


def create_cart(db: Session):
    db_cart = models.Cart()
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


def get_cart(db: Session, cart_id: int):
    cart = (
        db.query(models.Cart)
        .options(joinedload(models.Cart.items))
        .filter(models.Cart.id == cart_id)
        .first()
    )
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")

    total_cost = 0
    cart_items_data = []

    for cart_item in cart.items:
        item = cart_item.item
        subtotal = item.price * cart_item.quantity
        total_cost += subtotal

        cart_item_data = CartItemDisplay(
            item_id=item.id,
            quantity=cart_item.quantity,
            item=ItemDisplay(
                id=item.id,
                name=item.name,
                price=item.price,
                description=item.description,
                thumbnail=item.thumbnail,
                stock=item.stock,
                type=item.type,
                subtotal=subtotal,
            ),
            subtotal=subtotal,
        )
        cart_items_data.append(cart_item_data)

    return CartDisplay(id=cart.id, items=cart_items_data, total=total_cost)


def delete_cart(db: Session, cart_id: int):
    db_cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if db_cart:
        db.delete(db_cart)
        db.commit()
        return True
    return False


def get_carts(db: Session):
    carts = db.query(models.Cart).options(joinedload(models.Cart.items)).all()
    carts_data = []

    for cart in carts:
        total_cost = 0
        cart_items_data = []

        for cart_item in cart.items:
            item = cart_item.item
            subtotal = item.price * cart_item.quantity
            total_cost += subtotal

            cart_item_data = CartItemDisplay(
                item_id=item.id,
                quantity=cart_item.quantity,
                item=ItemDisplay(
                    id=item.id,
                    name=item.name,
                    price=item.price,
                    description=item.description,
                    thumbnail=item.thumbnail,
                    stock=item.stock,
                    type=item.type,
                    subtotal=subtotal,
                ),
                subtotal=subtotal,
            )
            cart_items_data.append(cart_item_data)

        cart_data = CartDisplay(id=cart.id, items=cart_items_data, total=total_cost)
        carts_data.append(cart_data)

    return carts_data


def add_item_to_cart(db: Session, cart_id: int, cart_item_data: CartItemCreate):
    item = (
        db.query(models.Item).filter(models.Item.id == cart_item_data.item_id).first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.stock < cart_item_data.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    item.stock -= cart_item_data.quantity
    cart_item = models.CartItem(
        cart_id=cart_id,
        item_id=cart_item_data.item_id,
        quantity=cart_item_data.quantity,
    )
    db.add(cart_item)
    db.commit()
    return cart_item


def remove_item_from_cart(
    db: Session, cart_id: int, item_id: int, quantity: int | None = None
):
    cart_item = (
        db.query(models.CartItem)
        .filter(models.CartItem.cart_id == cart_id, models.CartItem.item_id == item_id)
        .first()
    )

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    if quantity is not None and quantity > cart_item.quantity:
        raise HTTPException(
            status_code=400, detail="Trying to remove more items than are in the cart"
        )

    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if quantity is None or quantity >= cart_item.quantity:
        item.stock += cart_item.quantity
        db.delete(cart_item)
    else:
        cart_item.quantity -= quantity
        item.stock += quantity

    db.commit()
