from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.inventory.models.Item import Item
from app.modassembly.database.get_session import get_session
from app.modassembly.authentication.core.authenticate import authenticate
from app.models.User import User

router = APIRouter()

class ItemCreate(BaseModel):
    name: str = Field(..., title="Name of the item", max_length=100)
    description: str = Field("", title="Description of the item", max_length=255)
    quantity: int = Field(0, title="Quantity of the item", ge=0)

@router.post("/items", response_model=ItemCreate, status_code=status.HTTP_201_CREATED)
def add_item(
    item: ItemCreate,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(authenticate)]
) -> ItemCreate:
    """
    Add a new item to the inventory.

    - **name**: Name of the item (required, max length 100)
    - **description**: Description of the item (optional, max length 255)
    - **quantity**: Quantity of the item (optional, defaults to 0, must be non-negative)
    """
    db_item = Item(
        name=item.name,
        description=item.description,
        quantity=item.quantity
    )
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return ItemCreate(
        name=db_item.name.__str__(),
        description=db_item.description.__str__(),
        quantity=db_item.quantity.__int__()
    )
