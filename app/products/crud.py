from app.products.models import Product
from app.products.schemas import ProductCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging
from typing import List



logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,  # or DEBUG for even more logs
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)



def get_all_products_for_admin(db:Session, skip:int, page_size:int,current_user:dict)-> List[Product]:
    """Get all products added by the particular admin

    Args:
        db (Session): _description_
        skip (int): will tell the amount of records to skip to support page number
        page_size (int): will contain the number of records per page
        current_user (dict): User that is currently login as admin

    Returns:
        List[Product]: All products added by that admin
    """
    
    
    products = db.query(Product).filter(Product.admin_id==current_user["id"],
                                        Product.is_deleted==False).offset(skip).limit(page_size).all()
    return products


def add_product(product : ProductCreate, db : Session, current_user: dict)->dict:
    """Adding a product by admin

    Args:
        product (ProductCreate): A schema implement by pydantic to validate the new product details
        db (Session): A session object to communicate with db
        current_user (dict): Person that has currently logged in as Admin   

    Returns:
        dict: New product that has been added to the product table
    """
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



def get_product_by_id_for_admin(db: Session, product_id: int,current_user: dict)-> Product:
    """Admin tries to get a product added by him using product if

    Args:
        db (Session): An object used to communicate with db
        product_id (int): Product id of requested product 
        current_user (dict): Person that is currently logged in as admin

    Raises:
        HTTPException: 404-Product not found
        HTTPException: 403-Admin is trying to get the details of other admin's product

    Returns:
        Product: product record containing all product details as specified by model product
    """
    
    product = db.query(Product).filter(Product.id == product_id).first()


    if not product:
        logger.warning(f"Product with id : {product_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product with id : {product_id} not found")
    


    if product.admin_id != current_user['id']:
        logger.warning(f"Product with id:{product_id} does not belong to {current_user['email']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Product with id:{product_id} does not belong to {current_user['email']}")
    
    if product.is_deleted:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Product with id: {product_id} has already been deleted by admin {current_user['email']}")

    return product



def delete_product(product_id: int, db: Session, current_user: dict):
    """Deleting a product using id by admin

    Args:
        product_id (int): refers to the product id
        db (Session): A session obect that will communicate to the database
        current_user (dict): The user currently logged in Admin

    Raises:
        HTTPException: 404-No Product found
        HTTPException: 403-Admin is trying to delete another admin's product

    Returns:
            bool  : True means deletion succesfull
    """     

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        # logger.warning(f"No product fount for product with id {product_id} ")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No product fount for product with id {product_id} ")
    
    if product.admin_id != current_user['id']:
        logger.warning(f"{current_user['email']} is not the one who created product with id : {product_id}. Therefore he cannot update it")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not the one who created it. Therefore You cannot update it")
    
    if product.is_deleted==True:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"This product has already been deleted by admin {current_user['email']}")
    

    product.is_deleted=True
    db.commit()
    return True


def update_product(existing_product : Product, product : ProductCreate, db:Session)->Product:
    """Updation of product by admin using product id

    Args:
        existing_product (Product): is a product already available in db
        product (ProductCreate): is a pydantic product coming from user          
        db (Session): A Session object to communicat with db    

    Returns:
        Product: an updated product of type model Product
    """
    
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

def get_products_based_on_search(keyword: str, db: Session, skip: int, page_size: int )->List[Product]:
    """User tries to search for a keyword in database

    Args:
        keyword (str): A target keyword to search the product based on it
        db (Session): A Session Object that communicated with db
        skip (int): defines the number of records to skip . It has been already calculated using formula for page
        page_size (int): Defines number of records per page

    Returns:
        List[Product]: A collection of matched products with the keyword provided by user
    """



    query = db.query(Product).filter(Product.name.like(f"%{keyword}%"),
                                     Product.is_deleted==False)
    
    products = query.offset(skip).limit(page_size).all()
    if not products:
        # logger.warning(f"No product found for search keyword {keyword}")
        # return {"message": "No products found with the given keyword."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No products found with the given keyword {keyword}.")
    return products



def get_product_by_id( db : Session, product_id : int)->Product:
    """User is trying to get the product by its id

    Args:
        db (Session): A session object to connect with db and retrieve data
        product_id (int): refers to the product to be retrieved

    Raises:
        HTTPException: 404-Product Not Found

    Returns:
        Product: a model product having the same product_id
    """
    
    product = db.query(Product).filter(Product.id == product_id).first()


    if not product:
        logger.warning(f"Product with id : {product_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product with id : {product_id} not found")

    if product.is_deleted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="This product has been delelted by admin")

    return product



def get_all_products_for_user(category: str, min_price: float, max_price: float, sort_by: str, page: int, page_size: int, db: Session)->List[Product]:
    """Getting all products for user

    Args:
        category (str): defines the category of products to be retrieved
        min_price (float): price should be greater than it
        max_price (float): price should be smaller than it
        sort_by (str): sorting the orders based on name | category | price
        page (int): defines the page number
        page_size (int): number of products in a page
        db (Session): A object that handles db transactions

    Returns:
        List[Product]: contains all products satisfied all upper criterias
    """
    skip = (page - 1) * page_size


    query = db.query(Product).filter(
        Product.price >= min_price,
        Product.price <= max_price,
        Product.category.like(f"%{category}%"),
        Product.is_deleted == False
    )
    if sort_by == "name":
        query = query.order_by(Product.name)
    elif sort_by == "price":
        query = query.order_by(Product.price)
    elif sort_by == "category":
        query = query.order_by(Product.category)

    products = query.offset(skip).limit(page_size).all()

   
    
    return products