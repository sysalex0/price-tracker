# This is a sample Python script.
from config.db_config import init_db
from constant.Enums import Platform
from service.PriceTrackingService import fetch_and_save_new_products, notify_new_good_deals

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
price_tracking_configs = [
    {
        'tracking_keyword': 'airpod pro 2',
        'platforms': [Platform.CAROUSELL],
        'price_lower_bound': 900,
        'target_price_below': 1200
    }
]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init_db()
    fetch_and_save_new_products(price_tracking_configs)
    notify_new_good_deals(price_tracking_configs)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
