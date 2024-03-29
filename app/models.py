from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Item(Base):
    __tablename__: str = "item"
    id: Column = Column(Integer, primary_key=True)
    name: Column = Column(String, index=True)
    price: Column = Column(Float)
    description: Column = Column(String)
    thumbnail: Column = Column(String)
    stock: Column = Column(Integer, default=0)
    type: Column = Column(String)

    __mapper_args__: dict = {"polymorphic_identity": "item", "polymorphic_on": type}


class Product(Item):
    __mapper_args__: dict = {
        "polymorphic_identity": "product",
    }


class Event(Item):
    __mapper_args__: dict = {
        "polymorphic_identity": "event",
    }


class Cart(Base):
    __tablename__: str = "cart"
    id: Column = Column(Integer, primary_key=True)
    items: relationship = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__: str = "cart_item"
    cart_id: Column = Column(Integer, ForeignKey("cart.id"), primary_key=True)
    item_id: Column = Column(Integer, ForeignKey("item.id"), primary_key=True)
    quantity: Column = Column(Integer)
    cart: relationship = relationship("Cart", back_populates="items")
    item: relationship = relationship("Item")
