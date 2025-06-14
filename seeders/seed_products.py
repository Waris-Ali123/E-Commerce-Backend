# seed_products.py
from app.core.database import SessionLocal
from app.products.models import Product
from app.products.schemas import ProductCreate
# from app.core.database import

def seed_products():
    db = SessionLocal()
    try:
        products_data = [
            {
                "name": "Smartphone",
                "description": "Android smartphone with 6.5-inch display",
                "price": 12999.99,
                "stock": 100, 
                "category": "Electronics",
                "image_url": "https://example.com/smartphone.jpg",
                "admin_id": 1  # Make sure this admin exists!
            },
            {
                "name": "Laptop",
                "description": "Lightweight laptop with 16GB RAM",
                "price": 55999.50,
                "stock": 50,
                "category": "Computers",
                "image_url": "https://example.com/laptop.jpg",
                "admin_id": 1
            },
            {
                "name": "Wireless Earbuds",
                "description": "Noise-cancelling earbuds with long battery life",
                "price": 2999.00,
                "stock": 200,
                "category": "Accessories",
                "image_url": "https://example.com/earbuds.jpg",
                "admin_id": 1
            }
        ]

        for item in products_data:
            # productCreateDto = ProductCreate(**item)
            # product = item.dict()

            # admin_id = ,
            admin_id=item["admin_id"]
           
            product = ProductCreate(
            name=item["name"],
            description=item["description"],
            price=item["price"],
            stock=item["stock"],
            category=item["category"],
            image_url=item["image_url"]
            )

            new_product = Product(
                name=product.name,
                description=product.description,
                price=product.price,
                stock=product.stock,
                category=product.category,
                image_url=product.image_url,
                admin_id= admin_id # Assuming current_user is a dict with user details
            )
            db.add(new_product)

        db.commit()
        print(" Product data seeded!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_products()