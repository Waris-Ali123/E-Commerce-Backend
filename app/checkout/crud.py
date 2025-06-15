import logging.config
from sqlalchemy.orm import Session
from app.cart.models import Cart
from app.cart.schemas import CartOut
from app.orders.models import Order,OrderItem,Status
from datetime import datetime
from fastapi import HTTPException,status
from app.products.models import Product
import logging



logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,  # or DEBUG for even more logs
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s" 
)


def checkout_service(db : Session, current_user : dict)->Order:
    """Checking our for a user, removing all items from cart and generating new order

    Args:
        db (Session): An object that handles db operations
        current_user (dict): containing all logged in user details

    Raises:
        HTTPException: 404-Cart contains Nothing for current user   
        HTTPException: 400-Ordered quantity is more than the stock of that product

    Returns:
        Order: A new order containing all details of order items
    """

    logger.info(f"User {current_user['email']} is checking out ")

    current_user_id = current_user['id']
    #Filtering cart item and showing only that are not delelted by admin as well
    user_carts = db.query(Cart).filter(Cart.user_id == current_user['id']).join(Product, Cart.product_id == Product.id).all()

    if not user_carts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User cart is empty")
        

    total = 0
    order_items_local = []
    deleted_items = []

    for cart in user_carts:

        product = db.query(Product).filter(Product.id == cart.product_id).first()

        if not product :
            logger.error(f"Product with id {cart.product_id} has not been found in the cart with id : {cart.id} for the user {current_user['email']}")
            continue

        if product.is_deleted:
            logger.error(f"Cart item with product id : {product.id} is already deleted by admin")
            deleted_items.append(CartOut.from_orm(cart))
            continue



        if product.stock < cart.quantity:
            # logger.warn(f"User {current_user['email']} has put more quantity of product with id {product.id} than its stock : {product.stock}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Product with id {product.id} has only {product.stock} available. Change the quantity {cart.quantity}")
        
        product.stock -= cart.quantity

        subtotal = cart.quantity * product.price

        total += subtotal 

        order_item = OrderItem(product_id = cart.product_id,quantity = cart.quantity,price_at_purchase = product.price)

        order_items_local.append(order_item)


    new_order = Order(
        user_id = current_user_id,  
        total_amount = total,
        status = Status.PENDING.value,
        created_at = datetime.utcnow())   

    db.add(new_order)

    db.flush()


    logger.info(f"New Order has been created now the order items are being added")

    for o_item in order_items_local:
        o_item.order_id = new_order.id
        db.add(o_item)


    #Removing all deleted items and non deleted from user's cart
    db.query(Cart).filter(Cart.user_id == current_user_id).delete()
    db.commit()
    db.refresh(new_order)


    logger.info(f"New Order has been placed Successfully with order id : {new_order.id}")
    logger.info(f"{deleted_items}")
 
    return new_order,deleted_items