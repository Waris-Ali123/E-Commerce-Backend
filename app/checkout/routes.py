from fastapi import APIRouter,Depends, status
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.auth.permissions import only_user_allowed
from app.orders.schemas import OrderOutWithOrderItems
from app.checkout.schemas import CheckoutResponse

router = APIRouter()


@router.get("/checkout",response_model=CheckoutResponse,status_code=status.HTTP_200_OK)
def checking_Out(db : Session = Depends(get_db),current_user : dict = Depends(only_user_allowed)):
    from app.checkout.crud import checkout_service
    order,deleted_items = checkout_service(db,current_user)
    msg = "Checkout Is Successfull"


    if len(deleted_items)>0:
        msg += f" Only {len(deleted_items)} item(s) not been checked out bcz they had been deleted by admin"
    return {"order" : order,
            "deleted_items" : deleted_items,
            "msg" : msg
            }


