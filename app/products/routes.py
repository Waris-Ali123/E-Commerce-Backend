from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from app.core.database import get_db
# from app.auth.permissions import get_current_user, admin_required
from app.products.schemas import ProductCreate

router = APIRouter()

@router.get("/getAllProducts")
def get_products(db : Session =Depends(get_db)):
    from app.products.crud import get_all_products
    products = get_all_products(db)
    return products


@router.post("/addProduct", status_code=status.HTTP_201_CREATED)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    from app.products.crud import add_product as add_product_service
    new_product = add_product_service(product, db)
    return new_product