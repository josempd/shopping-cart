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


@app.delete("/carts/{cart_id}")
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    success = crud.delete_cart(db=db, cart_id=cart_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart not found")
    return JSONResponse(
        status_code=200, content={"message": "Cart deleted successfully"}
    )
