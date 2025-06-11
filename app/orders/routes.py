from fastapi import APIRouter,Depends, Path
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.auth.permissions import only_user_allowed
from app.orders.crud import order_history_service,get_single_order_serive
from app.orders.schemas import OrderOutWithOrderItems,OrderOutWithoutOrderItems 
from typing import List 


router = APIRouter(
    prefix="/orders"
)


@router.get("/",response_model=List[OrderOutWithoutOrderItems])
def get_complete_order_history(db: Session = Depends(get_db),current_user : dict = Depends(only_user_allowed)):
    order_history = order_history_service(db,current_user)
    return order_history


@router.get("/{order_id}",response_model=OrderOutWithOrderItems)
def get_particular_order(order_id : int = Path(...,ge=1) ,db: Session = Depends(get_db),current_user : dict = Depends(only_user_allowed)):
    single_order_history = get_single_order_serive(order_id,db,current_user)
    return single_order_history