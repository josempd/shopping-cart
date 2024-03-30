# Technical Test for Backend Developer at BlueQuo

## **Requirements**

We need to develop a shopping cart (API only). The system must allow adding items to the cart, modifying their quantity, and removing any item, in addition to allowing the retrieval of the cart's invoice with the totals and subtotals for each item.

| Item Name                     | Item Type | Units | Unit Price | Subtotal |
| ----------------------------- | --------- | ----- | ---------- | -------- |
| Tortoiseshell Sunglasses      | Product   | 3     | €39.99     | €119.97  |
| Red Hot Chili Peppers in Madrid | Event    | 5     | €60.00     | €300.00  |

Total: €419.97

If an item that already exists in the cart is added, the system must increase the units of that item. If the units of an item are reduced to 0, the item must be removed from the cart.

At all times, it must control the stock of each of the items, prohibiting the addition of items to the cart that do not have stock.

We have two types of items: events and products. Both types have specific attributes but share the attributes of price, name, thumbnail, and description.

## **Implementation**

- Design data model, classes, and persistence.
- Design of the URL structure or API schema explaining the behavior of each endpoint.
- Explanation of error management.

The following points will be valued:

- Implementation of REST API or GraphQL.
- Tests.
- Virtualizing or dockerizing the project.
- Although not essential, the use of the Python language will be valued.

Document the entire process and comment on the weak points, problems you have had, and how you would improve the system. It is not necessary to complete the entire test, but an explanation of how it would have been implemented will be valued.

---

## **Tech stack**

Defining a clear tech stack is important for project clarity and ease of development. This is also a core piece of the documentation and enables to have a proper feedback loop if necessary.

### **Core**

**Package Manager**: Poetry.

**Framework**: FastAPI.

**Database System**: PostgreSQL.

**ORM**: SQLAlchemy.

### **Testing**

**Unit Testing**: Pytest for writing test suites.

**Integration Testing**: TestClient from FastAPI.

### **Containerization & Virtualization**

**Containerization**: Docker.

**Container Orchestration**: Docker Compose.

### **Initial setup**

First we should setup the local environment:

```
python3 -m venv .venv
```
And to run it:
```
source .venv/bin/activate
```
Also, we can install pipx and then install poetry, for our package management:
```
pip install pipx
```
```
pipx install poetry
```

With poetry installed we can now start installing dependencies and setting up the necessary directories for the project:
- add dev dependencies:
    - ruff
    - pre-commit

- add project dependencies:
    - add fastapi
    - add uvicorn
    - add sqlalchemy
    - add python-dotenv
    - add psycopg2-binary

more dependencies will be added as needed.

### **Setup a base dockerfile and docker-compose**

The main two steps to guarantee virtualization of the app:

- Setting up a base dockerfile that has python, install poetry and setup the files in a container to make the app available to a docker-compose orchestrator.

- Setting up a docker-compose file with a postgres database with volumes to guarantee persistance, proper environment variables and that also includes the base image for the FastAPI server

### **Directory structure**

The proposed directory structure is the following, as it's simple and straightforward:

```
bluequo-challenge/
│
├── app/                    # Application specific components
│   ├── __init__.py         # Makes app a Python package
│   ├── main.py             # FastAPI application instance, routes, and startup events
│   ├── models.py           # SQLAlchemy models
│
├── .gitignore              # gitignore file
├── .pre-commit-config.yaml # pre-commit config file
├── .env                    # env file with secret values
├── Dockerfile              # Container specification
├── LICENSE                 # License agreement
├── poetry.lock             # Project dependencies
├── pyproject.toml          # Project dependencies
└── README.md               # Project overview and instructions
```

This structure will be updated overtime as the project advances.

### **Defining data models**

The models are defined using the declarative system, which allows the structure of the database to be described in Python code.

- Base Model: At the beginning, Base is created using declarative_base(). This serves as a base class for all models, allowing them to be automatically mapped to a database table.
- Item Model: Represents a generic item. It's designed to be a base class for more specific types of items.
- Product Model: Inherits from Item. It's a more specific type of item.
- Event Model: Another subclass of Item, representing an event, which is a different type of item.
- Cart Model: Represents a shopping cart.
- CartItem Model: Represents a many-to-many relationship between Cart and Item through an association table.

The data model will be refined as the project advances.

### **Setting up the database**

After the models are defined, then we can setup the database adapted to the model, doing the following:

- Updating models.py to adapt to latest sqlalchemy typing recommendations
- Create a database.py script that will use the sqlalchemy engine and the models to access the database
- creating an init_db.py script that creates the connection instance
- Creating a wait-for-db script so the backend service waits for the database to be ready to accept connections
- Setting up an entrypoint script to run everything
- Fixing the Dockerfile, pyproject and docker-compose to properly run around the entrypoint script
