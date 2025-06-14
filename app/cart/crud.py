from sqlalchemy.orm import Session
from app.products.models import Product
from app.cart.models import Cart 
from fastapi import  HTTPException, status
import logging
from typing import List



logger = logging.getLogger()

def adding_product_to_cart_service(product_id: int,quantity: int,current_user: dict, db : Session)->Cart:
    """User adding a product in cart

    Args:
        product_id (int): refers to the item id to be added in cart
        quantity (int): refers to the quantity of item
        current_user (dict): contains all logged in user details like name role etc
        db (Session): An object to communicate with db

    Raises:
        HTTPException: 404- No product found for product_id

    Returns:
        Cart: An object containing all details of user and product as well that has been added to the cart
    """
    logger.info(f"User {current_user['email']} is trying to add product with id : {product_id} in cart")
    existing_product = db.query(Product).filter(Product.id==product_id).first()
    if not existing_product :
        # logger.warn(f"No product found with id : {product_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No products found for product id : {product_id} ")
    
    if existing_product.is_deleted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Product with id: {product_id} has already been deleted by admin")


    is_already_available_in_cart = db.query(Cart).filter(Cart.user_id == current_user['id'] ,Cart.product_id==product_id).first()

    if is_already_available_in_cart :
        logger.info(f"Since the product with id {product_id} is already been added to user's cart thus modifying its quantity ")
        return updating_cart_item(product_id,quantity,db,current_user)

    new_cart = Cart(user_id = current_user['id'],
                    product_id = product_id,
                    quantity = quantity) 

    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    logger.info(f"The product is added to the cart successfully")
    return new_cart

    

        
def show_cart_items(db : Session,current_user: dict)->List[Cart]:
    """Showing all items to current user

    Args:
        db (Session): An object to communicate with db
        current_user (dict): All user details who is logged in now 

    Raises:
        HTTPException: 404-User Cart is empty

    Returns:
        List[Cart]: A collection that will contain all cart items that has been added to the cart
    """
    
    cart_items = db.query(Cart).join(Product, Cart.product_id == Product.id).filter(Cart.user_id == current_user['id']).all()

    if not cart_items:
        # logger.info("No items found in cart")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Cart is Empty")
    
    return cart_items





def deleting_cart_item(product_id: int, db : Session , current_user: dict)->dict:
    """User removes an item from cart

    Args:
        product_id (int): refers to the id of product
        db (Session): an object to contact with db
        current_user (dict): Containing all User details like name , role etc

    Raises:
        HTTPException: 404-Cart does not contain an item with id product_id

    Returns:
        dict: success msg indicating that the item has been removed from cart
    """
    
    item_to_be_deleted = db.query(Cart).filter(Cart.product_id == product_id,
                                               Cart.user_id == current_user['id']).first()
    
    if not item_to_be_deleted:
        # logger.info(f"Cart does not have any item with id : {product_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"product with product id : {product_id} is not inside the cart"
        )
    
    db.delete(item_to_be_deleted)
    db.commit()
    logger.info(f"Cart item with id : {product_id} is deleted successfully")

    return {"msg" : f"The cart item with id {product_id} has been deleted successfully"}

    

def updating_cart_item(product_id : int,quantity : int,db : Session, current_user : dict)->Product:
    """User updating a cart item 

    Args:
        product_id (int): id of product to be updated in cart
        quantity (int): updated quantity of product
        db (Session): An Object that handles all db operations
        current_user (dict): contains all user details like name and role

    Raises:
        HTTPException: 404-product with product_id is not present in the user's cart

    Returns:
        Product: An updated cart with updated quantity
    """




    logger.info(f"Current user {current_user['email'] } is trying to update the cart item with id  : {product_id}")
    existing_item_in_cart = db.query(Cart).filter(Cart.user_id == current_user['id'] ,Cart.product_id==product_id).first()

    if not existing_item_in_cart :
        # logger.warning(f"No cart item found with product id: {product_id} for user {current_user['email']}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Cart does not contains any item with id : {product_id}")


    if existing_item_in_cart.product.is_deleted:
        # logger.warning(f"Since the cart item having product with id: {existing_item_in_cart.product_id} is deleted by admin thus deleting it from cart too..")
        # deleting_cart_item(product_id,db,current_user)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Cart item with id: {existing_item_in_cart.product_id} has been removed by the admin")


    existing_item_in_cart.quantity = quantity
    db.commit()
    db.refresh(existing_item_in_cart)
    logger.info(f"The cart is modified successfully ")
    return existing_item_in_cart
