from abc import ABC, abstractmethod

from config.db_config import Session


class PriceTracker(ABC):
    SEARCH_KEYWORD_PLACEHOLDER_PATTERN = '{search_keyword}'

    @property
    @abstractmethod
    def crawl_base_url(self):
        pass

    @property
    @abstractmethod
    def platform(self):
        pass

    @abstractmethod
    def extract_products(self):
        pass

    @abstractmethod
    def filter_existed_products(self, products):
        pass


    def save_products(cls, products):
        # session = Session()
        with Session() as session:
            session.add_all(products)
            session.commit()

