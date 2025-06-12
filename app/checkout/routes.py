from fastapi import APIRouter,Depends, status
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.auth.permissions import only_user_allowed
from app.orders.schemas import OrderOutWithOrderItems


router = APIRouter()


@router.get("/checkout",response_model=OrderOutWithOrderItems,status_code=status.HTTP_200_OK)
def checking_Out(db : Session = Depends(get_db),current_user : dict = Depends(only_user_allowed)):
    from app.checkout.crud import checkout_service
    order = checkout_service(db,current_user)
    return order


