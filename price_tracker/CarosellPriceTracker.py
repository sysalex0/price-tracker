import re
import urllib.parse
from datetime import timedelta, datetime, timezone

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from constant.Enums import Currency, Platform
from model.Product import Product
from price_tracker.PriceTracker import PriceTracker


class CarosellPriceTracker(PriceTracker):
    @property
    def crawl_base_url(self):
        return 'https://www.carousell.com.hk/search/{search_keyword}?addRecent=true'

    @property
    def platform(self):
        return Platform.CAROUSELL

    def extract_products(self, tracking_keyword):
        url_encoded_keyword = urllib.parse.quote(tracking_keyword)
        search_url = self.crawl_base_url.replace(self.SEARCH_KEYWORD_PLACEHOLDER_PATTERN, url_encoded_keyword)
        ua = UserAgent()
        headers = {'User-Agent': str(ua.chrome)}

        response = requests.get(search_url, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        products_soup_result = soup.find_all('div', attrs={
            'data-testid': lambda value: value and re.match(r'listing-card-\d+', value)})

        # Print the found div elements
        products = []
        for product in products_soup_result:
            raw_product = self.extract_raw_product_from_soup(product)
            product = self.to_product_model(raw_product)
            products.append(product)

        return products

    def extract_raw_product_from_soup(self, product_soup_result):
        # get raw data
        # div[1]/a[2]
        url = 'https://www.carousell.com.hk' + product_soup_result.find_all('div')[0].find_all('a')[1].get('href')
        # div[1]/a[2]/p[1]/text()
        title = product_soup_result.find_all('div')[0].find_all('a')[1].find_all('p')[0].get_text(strip=True)
        if title == 'Bumped':
            # div[1]/a[2]/p[2]/text()
            title = product_soup_result.find_all('div')[0].find_all('a')[1].find_all('p')[1].get_text(strip=True)

        # div[1]/a[2]/div[2]/p
        raw_price = product_soup_result.find_all('div')[0].find_all('a')[1].find('p', attrs={
            'title': lambda value: value and re.match(r'\w+\$\d+', value)}).get('title')
        # div[1]/a[1]/div[2]/div/p
        raw_relative_time = product_soup_result.find_all('div')[0].find_all('a')[0].find('p', text=re.compile(
            r'\d+ \w+ ago')).get_text(strip=True)

        raw_product = {
            'title': title,
            'url': url,
            'price': raw_price,
            'relative_time': raw_relative_time
        }
        # print(raw_product)
        return raw_product

    def to_product_model(self, raw_product):
        # process
        match = re.match(r"(\w+)\$(\d+)", raw_product['price'])
        raw_currency = match.group(1)

        title = raw_product['title'].strip()
        currency = self.to_currency(raw_currency)
        price = float(match.group(2))
        url = raw_product['url'].strip()
        posting_time = self.convert_relative_time_to_datetime(raw_product['relative_time'])

        return Product(
            platform=self.platform,
            title=title,
            currency=currency,
            price=price,
            url=url,
            posting_time=posting_time,
        )

    def convert_relative_time_to_datetime(self, raw_time):
        def timedelta_years_months(years, months):
            total_days = int(years * 365.25 + months * 30.4375)
            return timedelta(days=total_days)

        pattern = r'(\d+)\s+(second|minute|hour|day|month|year)s?\s+ago'
        match = re.match(pattern, raw_time)
        if match:
            quantity = int(match.group(1))
            unit = match.group(2)
            if unit == 'second':
                delta = timedelta(seconds=quantity)
            elif unit == 'minute':
                delta = timedelta(minutes=quantity)
            elif unit == 'hour':
                delta = timedelta(hours=quantity)
            elif unit == 'day':
                delta = timedelta(days=quantity)
            elif unit == 'month':
                delta = timedelta_years_months(0, quantity)
            elif unit == 'year':
                delta = timedelta_years_months(quantity, 0)
            return datetime.now(timezone.utc) - delta
        else:
            return None

    def to_currency(self, raw_currency):
        match raw_currency:
            case 'HK':
                currency = Currency.HKD
        return currency

    def filter_existed_products(self, products):
        return products

