from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Query
from app.products.schemas import ProductOut


from app.core.database import get_db
# from app.auth.permissions import get_current_user, admin_required
from app.products.schemas import ProductCreate
from app.auth.permissions import get_current_user, admin_required


router = APIRouter()

@router.get("/admin/products/", response_model=list[ProductOut])
def get_products(db : Session =Depends(get_db),current_user: dict = Depends(admin_required),
                page : int = Query(default=1,gt=0), page_size : int = Query(default=10, ge=1, le=100)):
    from app.products.crud import get_all_products_for_admin
    skip = (page - 1) * page_size
    products = get_all_products_for_admin(db, skip=skip, page_size=page_size)
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found")
    return products


@router.post("/admin/products/", status_code=status.HTTP_201_CREATED, response_model=ProductOut)
def add_product(product: ProductCreate, db: Session = Depends(get_db),current_user: dict = Depends(admin_required)):
    from app.products.crud import add_product as add_product_service
    new_product = add_product_service(product, db, current_user)
    return new_product


@router.get("/admin/products/{product_id}",response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db),current_user: dict = Depends(admin_required)):
    from app.products.crud import get_product_by_id
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.put("/admin/products/{product_id}",response_model=ProductOut, status_code=status.HTTP_200_OK)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db), current_user: dict = Depends(admin_required)):
    from app.products.crud import get_product_by_id, update_product as update_product_service
    existing_product = get_product_by_id(db, product_id)
    if not existing_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    print(current_user)
    if(existing_product.admin_id != current_user['id']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not the one who created it. Therefore You cannot update it")
    
    updated_product = update_product_service(existing_product,product, db)
    return updated_product


@router.delete("/admin/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: dict = Depends(admin_required)):
    from app.products.crud import delete_product as delete_product_service
    delete_response = delete_product_service(product_id, db,current_user)
    if not delete_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {"detail": "Product deleted successfully"}





@router.get("/products/search",response_model=list[ProductOut])
def get_product_by_keyword(keyword: str = Query(..., min_length=1),page : int = Query(default=1,gt=0), page_size : int = Query(default=10, ge=1, le=100),
                           db : Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    from app.products.crud import get_products_based_on_search
    skip = (page - 1) * page_size
    products = get_products_based_on_search(keyword, db, skip=0, page_size=100)

    return products


@router.get("/products/",response_model=list[ProductOut])
def get_all_products_by_user(page: int = Query(default=1, gt=0), page_size: int = Query(default=10, ge=1, le=100),
                             category : str = Query(default = ""),min_price: float = Query(default=0.0), max_price: float = Query(default=float('inf')),
                             sort_by : str = Query(default="name", regex="^(name|price|category)$"),
                     db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    from app.products.crud import get_all_products_for_user
    

    products = get_all_products_for_user(category, min_price, max_price, sort_by, page,page_size, db)
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found")
    return products


@router.get("/products/{product_id}",response_model=ProductOut)
def get_product_by_id(product_id: int, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    from app.products.crud import get_product_by_id
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


