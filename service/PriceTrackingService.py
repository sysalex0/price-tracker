from factory.PriceTrackerFactory import get_platform_price_tracker


def fetch_and_save_new_products(price_tracking_configs):
    for price_tracking_config in price_tracking_configs:
        for platform in price_tracking_config['platforms']:
            price_tracker = get_platform_price_tracker(platform)
            products = price_tracker.extract_products(price_tracking_config['tracking_keyword'])
            new_products = price_tracker.filter_existed_products(products)
            price_tracker.save_products(new_products)