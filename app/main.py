from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.products.routes import router as products_router
from app.cart.routes import router as cart_router
from app.orders.routes import router as order_router
from app.checkout.routes import router as checkout_router
from app.auth.models import User
from app.products.models import Product
from app.cart.models import Cart
from app.orders.models import Order,OrderItem
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)




  
app = FastAPI()


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(products_router, tags=["products"])
app.include_router(cart_router, tags=["carts"])
app.include_router(order_router,tags=["orders"])
app.include_router(checkout_router,tags=["checkingOut"])

 

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}