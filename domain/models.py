from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


class Item(Base):
    __tablename__ = "item"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    price: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String)
    thumbnail: Mapped[str] = mapped_column(String)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    type: Mapped[str] = mapped_column(String)

    __mapper_args__ = {"polymorphic_identity": "item", "polymorphic_on": type}


class Product(Item):
    __mapper_args__ = {
        "polymorphic_identity": "Product",
    }


class Event(Item):
    __mapper_args__ = {
        "polymorphic_identity": "Event",
    }


class Cart(Base):
    __tablename__ = "cart"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = "cart_item"
    cart_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cart.id"), primary_key=True
    )
    item_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("item.id"), primary_key=True
    )
    quantity: Mapped[int] = mapped_column(Integer)
    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")
    item: Mapped["Item"] = relationship("Item")
