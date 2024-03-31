from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import db_session

app = FastAPI()


def get_db():
    with db_session() as db:
        yield db


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/items/", response_model=schemas.ItemDisplay)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.create_item(db=db, item=item)
    return db_item


@app.get("/items/{item_id}", response_model=schemas.ItemDisplay)
def get_single_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db=db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/items/", response_model=list[schemas.ItemDisplay])
def list_items(db: Session = Depends(get_db)):
    items = crud.get_items(db=db)
    return items


@app.put("/items/{item_id}", response_model=schemas.ItemDisplay)
def update_item(
    item_id: int, item_update: schemas.ItemUpdate, db: Session = Depends(get_db)
):
    updated_item = crud.update_item(db=db, item_id=item_id, updated_item=item_update)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@app.delete("/items/", status_code=200)
def delete_items(request: schemas.ItemDeleteRequest, db: Session = Depends(get_db)):
    crud.delete_items(db=db, item_ids=request.item_ids)
    return {"message": "Item(s) deleted successfully"}


@app.post("/carts/", response_model=schemas.CartDisplay)
def create_cart(db: Session = Depends(get_db)):
    return crud.create_cart(db=db)


@app.get("/carts/", response_model=list[schemas.CartDisplay])
def list_carts(db: Session = Depends(get_db)):
    carts = crud.get_carts(db=db)
    return carts


@app.get("/carts/{cart_id}", response_model=schemas.CartDisplay)
def read_cart(cart_id: int, db: Session = Depends(get_db)):
    db_cart = crud.get_cart(db=db, cart_id=cart_id)
    if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return db_cart


@app.post("/carts/{cart_id}/items", response_model=schemas.CartItemDisplay)
def add_item_to_cart(
    cart_id: int, cart_item: schemas.CartItemCreate, db: Session = Depends(get_db)
):
    return crud.add_item_to_cart(db=db, cart_id=cart_id, cart_item_data=cart_item)


@app.delete("/carts/{cart_id}")
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    success = crud.delete_cart(db=db, cart_id=cart_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart not found")
    return JSONResponse(
        status_code=200, content={"message": "Cart deleted successfully"}
    )


@app.delete("/carts/{cart_id}/items", status_code=200)
def remove_item_from_cart(
    cart_id: int,
    remove_request: schemas.CartItemRemoveRequest,
    db: Session = Depends(get_db),
):
    crud.remove_item_from_cart(
        db=db,
        cart_id=cart_id,
        item_id=remove_request.item_id,
        quantity=remove_request.quantity,
    )
    return {"message": "Item removed from cart successfully"}
