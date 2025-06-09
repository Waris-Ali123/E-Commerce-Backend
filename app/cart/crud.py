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
        logger.info(f"The cart is modified successfully ")
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

    

        
def show_cart_items(db : Session,current_user):
    
    cart_items = db.query(Cart).filter(Cart.user_id == current_user['id']).all()

    if not cart_items:
        logger.info("No items found in cart")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="Nothing to see in cart")
    
    return cart_items





def deleting_cart_item(product_id, db : Session , current_user):
    
    item_to_be_deleted = db.query(Cart).filter(Cart.product_id == product_id,
                                               Cart.user_id == current_user['id']).first()
    
    if not item_to_be_deleted:
        logger.info(f"Cart does not have any item with id : {product_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"product with product id : {product_id} is not inside the cart"
        )
    
    db.delete(item_to_be_deleted)
    db.commit()
    logger.info(f"Cart item with id : {product_id} is deleted successfully")

    return {"msg" : f"The cart item with id {product_id} has been deleted successfully"}

    

def updating_cart_item(product_id,quantity,db, current_user):
    pass


    logger.info(f"Current user {current_user['email'] } is trying to update the cart item with id  : {product_id}")
    existing_item_in_cart = db.query(Cart).filter(Cart.user_id == current_user['id'] ,Cart.product_id==product_id).first()

    if not existing_item_in_cart :
        logger.warning(f"No cart item found with product id: {product_id} for user {current_user['email']}")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Cart does not contains any item with id : {product_id}")




    existing_item_in_cart.quantity = quantity
    db.commit()
    db.refresh(existing_item_in_cart)
    logger.info(f"The cart is modified successfully ")
    return existing_item_in_cart
