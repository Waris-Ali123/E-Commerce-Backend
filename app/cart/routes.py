from fastapi import APIRouter,Query, Depends
from app.auth.permissions import only_user_allowed
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.cart import crud

router = APIRouter()

@router.post("/cart")
def add_product_to_cart(product_id : int = Query(...),quantity : int = Query(default=1,gt=0), current_user : dict = Depends(only_user_allowed),db : Session = Depends(get_db)):
    product_added = crud.adding_product_to_cart_service(product_id,quantity,current_user,db)

    return product_added