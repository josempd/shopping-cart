from infrastructure.database import SessionLocal
from domain.models import Item

item_data = [
    # Products
    {
        "name": "Eco-Friendly Water Bottle",
        "price": 20.00,
        "description": "Stay hydrated in style with our durable and sustainable water bottle.",
        "thumbnail": "thumbnail_bottle.jpg",
        "stock": 3,
        "type": "Product",
    },
    {
        "name": "Bluetooth Noise-Canceling Headphones",
        "price": 89.99,
        "description": "Experience crystal-clear sound without distractions.",
        "thumbnail": "thumbnail_headphones.jpg",
        "stock": 5,
        "type": "Product",
    },
    {
        "name": "Organic Cotton Yoga Mat",
        "price": 45.00,
        "description": "Find your zen with our eco-friendly and comfortable yoga mat.",
        "thumbnail": "thumbnail_yogamat.jpg",
        "stock": 2,
        "type": "Product",
    },
    {
        "name": "Gourmet Coffee Beans",
        "price": 15.50,
        "description": "Start your day right with our premium, ethically sourced coffee beans.",
        "thumbnail": "thumbnail_coffee.jpg",
        "stock": 5,
        "type": "Product",
    },
    {
        "name": "Smart Indoor Herb Garden",
        "price": 120.00,
        "description": "Grow fresh herbs all year round with our automated indoor garden.",
        "thumbnail": "thumbnail_herbgarden.jpg",
        "stock": 1,
        "type": "Product",
    },
    # Events
    {
        "name": "Live Coding Workshop",
        "price": 50.00,
        "description": "Enhance your programming skills in our interactive coding workshop.",
        "thumbnail": "thumbnail_codingworkshop.jpg",
        "stock": 10,
        "type": "Event",
    },
    {
        "name": "Outdoor Photography Class",
        "price": 75.00,
        "description": "Capture the beauty of nature with tips from our expert photographer.",
        "thumbnail": "thumbnail_photography.jpg",
        "stock": 3,
        "type": "Event",
    },
    {
        "name": "Virtual Wine Tasting Experience",
        "price": 40.00,
        "description": "Discover and taste fine wines from the comfort of your home.",
        "thumbnail": "thumbnail_winetasting.jpg",
        "stock": 5,
        "type": "Event",
    },
    {
        "name": "Sustainable Living Webinar",
        "price": 0.00,
        "description": "Learn about sustainable living practices in our free webinar.",
        "thumbnail": "thumbnail_sustainable.jpg",
        "stock": 5,
        "type": "Event",
    },
    {
        "name": "Marathon for Charity",
        "price": 25.00,
        "description": "Join our charity marathon and help raise funds for a good cause.",
        "thumbnail": "thumbnail_marathon.jpg",
        "stock": 2,
        "type": "Event",
    },
]


def create_items(item_data):
    items = []
    for data in item_data:
        item = Item(**data)
        items.append(item)
    return items


def add_items_to_db(items, db_session):
    for item in items:
        db_session.add(item)
    db_session.commit()


def main():
    db = SessionLocal()
    if db.query(Item).count() == 0:
        items = create_items(item_data)
        add_items_to_db(items, db)
    else:
        db.close()


if __name__ == "__main__":
    main()
