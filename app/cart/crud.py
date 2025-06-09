from sqlalchemy.orm import Session
from app.products.models import Product
from app.cart.models import Cart 
from fastapi import  HTTPException, status
import logging



logger = logging.getLogger()

def adding_product_to_cart_service(product_id,quantity,current_user,db : Session):
    logger.info(f"User {current_user['email']} is trying to add product with id : {product_id} in cart")
    existing_product = db.query(Product).filter(Product.id==product_id).first()
    if not existing_product :
        logger.warn(f"No product found with id : {product_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No products found for product id : {product_id} ")


    is_already_available_in_cart = db.query(Cart).filter(Cart.user_id == current_user['id'] ,Cart.product_id==product_id).first()

    if is_already_available_in_cart :
        logger.info("The product is already in cart thus updating the quantity only")
        is_already_available_in_cart.quantity = quantity
        db.commit()
        db.refresh(is_already_available_in_cart)
        logger.infor(f"The cart is modified successfully ")
        # print(is_already_available_in_cart)
        return is_already_available_in_cart

    else:
        
        new_cart = Cart(user_id = current_user['id'],
                        product_id = product_id,
                        quantity = quantity) 

        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)
        logger.info(f"The product is added to the cart successfully")
        return new_cart

    

        
