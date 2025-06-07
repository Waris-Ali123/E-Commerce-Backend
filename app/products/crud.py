def get_all_products(db):
    from app.products.models import Product
    products = db.query(Product).all()
    return products


def add_product(product, db):
    from app.products.models import Product
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category=product.category,
        image_url=product.image_url
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product