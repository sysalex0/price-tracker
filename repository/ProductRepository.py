from sqlalchemy import select

from config.db_config import Session
from model.Product import Product


def find_first_by_platform_and_product_unique_id_order_by_price_asc(platform, product_unique_id):
    statement = select(Product)\
        .where(Product.platform == platform)\
        .where(Product.product_unique_id == product_unique_id)\
        .order_by(Product.price.asc())
    with Session() as session:
        product = session.scalars(statement).first()
        return product
