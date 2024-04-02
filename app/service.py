from fastapi import HTTPException
from sqlalchemy.orm import Session

from schemas.items import ItemCreate, ItemDisplay, ItemUpdate

from . import crud


def create_item_and_commit(db: Session, item_data: ItemCreate) -> ItemDisplay:
    new_item = crud.create_item(db, item_data)
    db.commit()
    db.refresh(new_item)
    return new_item


def get_item_service(db: Session, item_id: int) -> ItemDisplay:
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


def get_items_service(db: Session) -> list[ItemDisplay]:
    items = crud.get_items(db=db)
    return items


def update_item_service(
    db: Session, item_id: int, item_update: ItemUpdate
) -> ItemDisplay:
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    try:
        updated_item = crud.update_item(
            db=db, item_id=item_id, updated_item=item_update
        )
        db.commit()
        db.refresh(updated_item)
        return updated_item
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
