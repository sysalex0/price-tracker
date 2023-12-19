from model.Notification import Notification


def product_model_to_notification_model(product):
    return Notification(product_id=product.id)