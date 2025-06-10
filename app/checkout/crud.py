import logging.config
from sqlalchemy.orm import Session
from app.cart.models import Cart
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


def checkout_service(db : Session, current_user : dict):

    current_user_id = current_user['id']
    user_carts = db.query(Cart).filter(Cart.user_id==current_user_id).all()

    if not user_carts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User cart is empty")
        

    total = 0
    order_items_local = []

    for cart in user_carts:

        product = db.query(Product).filter(Product.id == cart.product_id).first()

        if not product :
            continue


        if product.stock < cart.quantity:
            logger.warn(f"User {current_user['email']} has put more quantity of product with id {product.id} than its stock : {product.stock}")
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"Product with id {product.id} has only {product.stock} available. Change the quantity {cart.quantity}")
        
        product.stock -= cart.quantity

        subtotal = cart.quantity * product.price

        total += subtotal 

        order_item = OrderItem(product_id = cart.product_id,quantity = cart.quantity,price_at_purchase = product.price)

        order_items_local.append(order_item)


    new_order = Order(
        user_id = current_user_id,  
        total_amount = total,
        status = Status.PENDING.value,
        created_at = datetime.now())   

    db.add(new_order)

    db.flush()

    for o_item in order_items_local:
        o_item.order_id = new_order.id
        db.add(o_item)



    db.query(Cart).filter(Cart.user_id == current_user_id).delete()
    db.commit()
    db.refresh(new_order)



    # new_order.order_items = order_items_local

    print(new_order)
     
    return new_order