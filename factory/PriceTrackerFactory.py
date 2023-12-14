from constant.Enums import Platform
from price_tracker.CarousellPriceTracker import CarousellPriceTracker

platform_price_tracker_dict = {
    Platform.CAROUSELL: CarousellPriceTracker()
}


def get_platform_price_tracker(platform):
    platform_price_tracker = platform_price_tracker_dict[platform]
    if platform_price_tracker is not None:
        return platform_price_tracker
    else:
        raise Exception('Unsupported platform')
