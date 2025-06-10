from fastapi import APIRouter,Query, Depends, status
from app.auth.permissions import only_user_allowed
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.cart import crud
from app.cart import schemas

router = APIRouter()

@router.post("/cart",response_model=schemas.CartOut)
def add_product_to_cart(product_id : int = Query(...),quantity : int = Query(default=1,gt=0), current_user : dict = Depends(only_user_allowed),db : Session = Depends(get_db)):
    product_added = crud.adding_product_to_cart_service(product_id,quantity,current_user,db)

    return product_added



@router.get("/cart",response_model=list[schemas.CartOut])
def get_cart_products(db : Session = Depends(get_db),current_user : dict = Depends(only_user_allowed)):
    cart_added_products = crud.show_cart_items(db,current_user)
    return cart_added_products



@router.delete("/cart/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(product_id : int , db : Session = Depends(get_db),current_user : dict = Depends(only_user_allowed)):
    msg = crud.deleting_cart_item(product_id,db,current_user)

    return msg



@router.put("/cart/{product_id}",status_code=status.HTTP_200_OK,response_model=schemas.CartOut)
def update_cart_item(product_id:int, quantity : int = Query(...,gt=0) ,db : Session = Depends(get_db),current_user : dict = Depends(only_user_allowed) ):
    updated_cart_item = crud.updating_cart_item(product_id,quantity,db, current_user)
    return updated_cart_item
