from constant.Enums import Platform
from price_tracker.CarousellPriceTracker import CarousellPriceTracker

platform_price_tracker_dict = {
    Platform.CAROUSELL: CarousellPriceTracker()
}


def get_platform_price_tracker(platform):
    if platform in platform_price_tracker_dict:
        return platform_price_tracker_dict[platform]
    else:
        raise Exception('Unsupported platform')
