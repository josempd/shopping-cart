from typing import Optional, List
from fastapi import HTTPException
from domain.models import CartItem
from schemas.cart import CartItemDisplay, CartDisplay
from domain.repo_interfaces import ICartRepository, IItemRepository

class CartService:
    def __init__(self, cart_repository: ICartRepository, item_repository: IItemRepository):
        self.cart_repository = cart_repository
        self.item_repository = item_repository

    def calculate_subtotal(self, quantity: int, price: float) -> float:
        """Calculate subtotal based on quantity and unit price."""
        return quantity * price

    def add_item_to_cart(self, cart_id: int, item_id: int, quantity: int):
        cart = self.cart_repository.get(cart_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        item = self.item_repository.get(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        if item.stock < quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")

        cart_item = self.cart_repository.get_cart_item(cart_id, item_id)
        if cart_item:
            self.cart_repository.update_cart_item(cart_id, item_id, {'quantity': cart_item.quantity + quantity})
        else:
            cart_item = CartItem(cart_id=cart_id, item_id=item_id, quantity=quantity)
            self.cart_repository.add_cart_item(cart_item)
        self.item_repository.update(item_id, {'stock': item.stock - quantity})

        subtotal = self.calculate_subtotal(quantity, item.price)

        cart_item_display = CartItemDisplay(
            item_id=cart_item.item_id,
            quantity=cart_item.quantity,
            item=item,
            subtotal=subtotal,
        )
        return cart_item_display

    def get_cart_details(self, cart_id: int) -> CartDisplay:
        cart = self.cart_repository.get(cart_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        items_display = []
        cart_total = 0

        for cart_item in cart.items:
            item = self.item_repository.get(cart_item.item_id)
            if item:
                subtotal = self.calculate_subtotal(cart_item.quantity, item.price)
                cart_total += subtotal

                items_display.append(
                    CartItemDisplay(
                        item_id=cart_item.item_id,
                        quantity=cart_item.quantity,
                        item=item,
                        subtotal=subtotal,
                    )
                )

        return CartDisplay(
            id=cart.id,
            items=items_display,
            total=cart_total,
        )

    def list_carts_with_details(self) -> List[CartDisplay]:
        carts = self.cart_repository.list()
        cart_displays = []

        for cart in carts:
            items_display = []
            cart_total = 0

            for cart_item in cart.items:
                item = self.item_repository.get(cart_item.item_id)
                if item:
                    subtotal = self.calculate_subtotal(cart_item.quantity, item.price)
                    cart_total += subtotal

                    items_display.append(
                        CartItemDisplay(
                            item_id=cart_item.item_id,
                            quantity=cart_item.quantity,
                            item=item,
                            subtotal=subtotal,
                        )
                    )

            cart_displays.append(
                CartDisplay(
                    id=cart.id,
                    items=items_display,
                    total=cart_total,
                )
            )

        return cart_displays

    def remove_item_from_cart(self, cart_id: int, item_id: int, quantity: Optional[int] = None):
        cart = self.cart_repository.get(cart_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        cart_item = self.cart_repository.get_cart_item(cart_id, item_id)
        if not cart_item:
            raise HTTPException(status_code=404, detail="Item not found in cart")

        item = self.item_repository.get(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        if quantity is not None and quantity > cart_item.quantity:
            raise HTTPException(status_code=400, detail=f"Cannot remove {quantity} items. Only {cart_item.quantity} available in cart.")

        if quantity is None or quantity >= cart_item.quantity:
            item.stock += cart_item.quantity
            self.cart_repository.remove_cart_item(cart_item)
        else:
            cart_item.quantity -= quantity
            item.stock += quantity
            self.cart_repository.update_cart_item(cart_id, item_id, {'quantity': cart_item.quantity})
