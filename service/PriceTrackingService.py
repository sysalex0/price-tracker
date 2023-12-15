from config.db_config import Session
from factory.PriceTrackerFactory import get_platform_price_tracker
from mapper.model_mapper import product_model_to_notification_model
from mapper.notification_mapper import product_to_html_message
from repository.NotificationRepository import find_notifications_by_product_ids
from repository.ProductRepository import find_products_by_platform_and_search_keyword_and_min_price, \
    find_products_by_platform_and_search_keyword_and_between
from service.NotificationService import send_message_to_telegram


def fetch_and_save_new_products(price_tracking_configs):
    for price_tracking_config in price_tracking_configs:
        for platform in price_tracking_config['platforms']:
            price_tracker = get_platform_price_tracker(platform)
            products = price_tracker.extract_products(price_tracking_config['tracking_keyword'])
            new_products = price_tracker.filter_new_or_lower_price_products(products)
            price_tracker.save_products(new_products)


def notify_new_good_deals(price_tracking_configs):
    for price_tracking_config in price_tracking_configs:
        products = []
        for platform in price_tracking_config['platforms']:
            if price_tracking_config['price_lower_bound'] is not None and price_tracking_config['target_price_below'] is not None:
                good_deals_in_platform = find_products_by_platform_and_search_keyword_and_between(
                    platform,
                    price_tracking_config['tracking_keyword'],
                    price_tracking_config['price_lower_bound'],
                    price_tracking_config['target_price_below']
                )
            else:
                good_deals_in_platform = find_products_by_platform_and_search_keyword_and_min_price(platform, price_tracking_config['tracking_keyword'])
            good_deals_in_platform_ids_set = set([product.id for product in good_deals_in_platform])
            notified_products = find_notifications_by_product_ids(good_deals_in_platform_ids_set)

            notified_product_ids_set = set([notified_product.product_id for notified_product in notified_products])
            product_ids_never_notified = good_deals_in_platform_ids_set - notified_product_ids_set
            products_never_notified = [product for product in good_deals_in_platform if product.id in product_ids_never_notified]
            products.extend(products_never_notified)

        for product in products:
            html_messages = product_to_html_message(product)
            send_message_to_telegram(html_messages)
            notification = product_model_to_notification_model(product)
            with Session() as session:
                session.add(notification)
                session.commit()
