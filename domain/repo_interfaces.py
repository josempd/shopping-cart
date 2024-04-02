from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Item, Cart, CartItem

class IItemRepository(ABC):
    @abstractmethod
    def create(self, item: Item) -> Item:
        """Create and return a new item."""
        pass

    @abstractmethod
    def get(self, item_id: int) -> Optional[Item]:
        """Retrieve an item by its ID. Returns None if not found."""
        pass

    @abstractmethod
    def list(self) -> List[Item]:
        """List all items."""
        pass

    @abstractmethod
    def update(self, item_id: int, item_data: dict) -> Optional[Item]:
        """Update an existing item. Returns the updated item, or None if not found."""
        pass

    @abstractmethod
    def delete(self, item_id: int) -> None:
        """Delete an item by its ID."""
        pass

class ICartRepository(ABC):
    @abstractmethod
    def create(self) -> Cart:
        """Create and return a new cart."""
        pass

    @abstractmethod
    def get(self, cart_id: int) -> Optional[Cart]:
        """Retrieve a cart by its ID. Returns None if not found."""
        pass

    @abstractmethod
    def list(self) -> List[Cart]:
        """List all carts."""
        pass

    @abstractmethod
    def delete(self, cart_id: int) -> None:
        """Delete an cart by its ID."""
        pass

    @abstractmethod
    def get_cart_item(self, cart_id: int, item_id: int) -> Optional[CartItem]:
        """Retrieve a CartItem by cart and item IDs. Returns None if not found."""
        pass

    @abstractmethod
    def add_cart_item(self, cart_item: CartItem) -> None:
        """Add a new CartItem to a cart."""
        pass

    @abstractmethod
    def remove_cart_item(self, cart_item: CartItem) -> None:
        """Remove a CartItem from a cart."""
        pass

    @abstractmethod
    def update_cart_item(self, cart_item: CartItem) -> None:
        """Update an existing CartItem."""
        pass

class ICartService(ABC):
    @abstractmethod
    def add_item_to_cart(self, cart_id: int, item_id: int, quantity: int) -> None:
        """Add an item to the specified cart."""
        pass

    @abstractmethod
    def remove_item_from_cart(self, cart_id: int, item_id: int, quantity: Optional[int] = None) -> None:
        """Remove an item from the specified cart."""
        pass
