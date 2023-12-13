from constant.Enums import Platform
from price_tracker.CarosellPriceTracker import CarosellPriceTracker

platform_price_tracker_dict = {
    Platform.CAROUSELL: CarosellPriceTracker()
}


def get_platform_price_tracker(platform):
    platform_price_tracker = platform_price_tracker_dict[platform]
    if platform_price_tracker is not None:
        return platform_price_tracker
    else:
        raise Exception('Unsupported platform')
