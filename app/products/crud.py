from app.products.models import Product
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging



logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,  # or DEBUG for even more logs
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)



def get_all_products_for_admin(db, skip, page_size,current_user):
    
    products = db.query(Product).filter(Product.admin_id==current_user["id"]).offset(skip).limit(page_size).all()
    return products


def add_product(product, db, current_user):
    
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category=product.category,
        image_url=product.image_url,
        admin_id= current_user['id']  # Assuming current_user is a dict with user details
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product



def get_product_by_id(db, product_id: int,current_user):
    
    product = db.query(Product).filter(Product.id == product_id).first()


    if not product:
        logger.warning(f"Product with id : {product_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product with id : {product_id} not found")


    if product.admin_id != current_user['id']:
        logger.warning(f"Product with id:{product_id} does not belong to {current_user['email']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Product with id:{product_id} does not belong to {current_user['email']}")
    return product



def delete_product(product_id: int, db, current_user):
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        logger.warning(f"No product fount for product with id {product_id} ")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No product fount for product with id {product_id} ")
    
    if product.admin_id != current_user['id']:
        logger.warning(f"{current_user['email']} is not the one who created product with id : {product_id}. Therefore he cannot update it")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not the one who created it. Therefore You cannot update it")
    
    db.delete(product)
    db.commit()
    return True


def update_product(existing_product : Product, product, db:Session):

    
    existing_product.name = product.name
    existing_product.description = product.description
    existing_product.price = product.price
    existing_product.stock = product.stock
    existing_product.category = product.category
    existing_product.image_url = product.image_url
    db.commit()
    db.refresh(existing_product)
    
    return existing_product


#Users functionalities

def get_products_based_on_search(keyword: str, db: Session,skip: int, page_size: int ):
    
    products = db.query(Product).filter(Product.name.like(f"%{keyword}%")).all()
    if not products:
        logger.warning(f"No product found for search keyword {keyword}")
        return {"message": "No products found with the given keyword."}
    return products



def get_all_products_for_user(category: str, min_price: float, max_price: float, sort_by: str, page: int, page_size: int, db: Session):
    skip = (page - 1) * page_size


    query = db.query(Product).filter(
        Product.price >= min_price,
        Product.price <= max_price,
        Product.category.like(f"%{category}%"),
    )
    if sort_by == "name":
        query = query.order_by(Product.name)
    elif sort_by == "price":
        query = query.order_by(Product.price)
    elif sort_by == "category":
        query = query.order_by(Product.category)

    products = query.offset(skip).limit(page_size).all()

   
    
    return products