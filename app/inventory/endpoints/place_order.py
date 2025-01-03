from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.inventory.models.Order import Order
from app.inventory.models.OrderItem import OrderItem
from app.inventory.models.Item import Item
from app.modassembly.database.get_session import get_session
from app.modassembly.authentication.core.authenticate import authenticate
from app.models.User import User

router = APIRouter()

class OrderItemRequest(BaseModel):
    item_id: int
    quantity: int

class OrderRequest(BaseModel):
    items: List[OrderItemRequest]

@router.post("/orders", response_model=OrderRequest)
def place_order(
    order_request: OrderRequest,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(authenticate)]
) -> OrderRequest:
    # Validate and create a new order
    new_order = Order(user_id=current_user.id.__int__())
    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    # Associate items with the order
    for item_request in order_request.items:
        item = session.query(Item).filter(Item.id == item_request.item_id).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_request.item_id} not found"
            )
        if item_request.quantity > item.quantity.__int__():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough quantity for item ID {item_request.item_id}"
            )
        order_item = OrderItem(
            order_id=new_order.id.__int__(),
            item_id=item.id.__int__(),
            quantity=item_request.quantity
        )
        session.add(order_item)
        # Update item quantity
        item.quantity = item.quantity.__int__() - item_request.quantity
    session.commit()

    return order_request
