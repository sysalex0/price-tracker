from sqlalchemy import select, func

from config.db_config import Session
from model.Product import Product


def find_first_product_by_platform_and_product_unique_id_order_by_price_asc(platform, product_unique_id):
    statement = select(Product) \
        .where(Product.platform == platform) \
        .where(Product.product_unique_id == product_unique_id) \
        .order_by(Product.price.asc())
    with Session() as session:
        product = session.scalars(statement).first()
        return product


def find_products_by_platform_and_search_keyword_and_between(platform, search_keyword, lower_bound, upper_bound):
    with Session() as session:
        return session.query(Product).filter(Product.price.between(lower_bound, upper_bound)).all()


def find_products_by_platform_and_search_keyword_and_min_price(platform, search_keyword):
    with Session() as session:
        min_price_products_subquery = session.query(func.min(Product.price))\
            .filter(Product.platform == platform, Product.search_keyword == search_keyword)\
            .scalar_subquery()

        # Query products with the lowest price, platform, and search keywords
        min_price_products = session.query(Product)\
            .filter(Product.price == min_price_products_subquery, Product.platform == platform, Product.search_keyword == search_keyword)

        return min_price_products.all()
