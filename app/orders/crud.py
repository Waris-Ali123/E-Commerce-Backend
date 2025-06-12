from sqlalchemy.orm import Session
from app.orders.models import Order
from fastapi import HTTPException,status
import logging

logger = logging.getLogger(__name__)

def order_history_service(db : Session , current_user):
    logger.info(f"User {current_user['email']} is trying to fetch all orders history")
    current_user_id = current_user['id']
    all_prev_orders = db.query(Order).filter(Order.user_id == current_user_id).all()

    if not all_prev_orders:
        logger.error(f"No order history found for {current_user['email']}")
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail="No orders found")
    

    logger.info(f"All orders' history fetched for {current_user['email']}")

    return all_prev_orders


def get_single_order_serive(order_id ,db : Session , current_user):
    
    logger.info(f"User {current_user['email']} is trying to fetch order's details with id {order_id}")
    current_user_id = current_user['id']
    order = db.query(Order).filter(Order.user_id == current_user_id,
                                   Order.id == order_id).first()

    if not order:
        logger.error(f"No order history found with id {order_id} for {current_user['email']}")
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"No order found with id : {order_id} for current_user {current_user['email']}")
    
    logger.info(f"Order history with id {order_id} fetched for {current_user['email']}")

    return order
