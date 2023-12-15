from sqlalchemy import select

from config.db_config import Session
from model.Notification import Notification


def find_notifications_by_product_ids(product_ids):
    statement = select(Notification) \
        .filter(Notification.product_id.in_(product_ids))
    with Session() as session:
        notification = session.scalars(statement)
        return notification.all()
