from sqlalchemy.orm import Session
from app.orders.models import Order
from fastapi import HTTPException,status

def order_history_service(db : Session , current_user):
    
    current_user_id = current_user['id']
    all_prev_orders = db.query(Order).filter(Order.user_id == current_user_id).all()

    if not all_prev_orders:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail="No orders found")
    

    return all_prev_orders


def get_single_order_serive(order_id ,db : Session , current_user):
    
    current_user_id = current_user['id']
    order = db.query(Order).filter(Order.user_id == current_user_id,
                                   Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"No order found with id : {order_id} for current_user {current_user['email']}")
    

    return order
