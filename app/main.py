from fastapi import Depends, FastAPI
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
