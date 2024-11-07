from app.models import Product

class ProductService:
    def get_all_products(self, db):
        """Retrieve all products"""
        return db.session.query(Product).all()

    def get_product_by_id(self, db, product_id):
        """Retrieve a product by its ID"""
        return db.session.query(Product).filter_by(id=product_id).first()

    def add_product(self, db, name, description, price):
        """Add a new product"""
        product = Product(name=name, description=description, price=price)
        db.session.add(product)
        db.session.commit()
        return product
