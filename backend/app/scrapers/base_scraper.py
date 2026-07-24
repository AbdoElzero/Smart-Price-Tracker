"""
BaseScraper: الكلاس الأساسي الذي يرث منه كل Scraper.

مثال:
    class BTechScraper(BaseScraper):
        store_slug = "btech"
        def fetch_prices(self):
            return [{"product_id": 1, "country_id": 2, "price": 15999.0, "in_stock": True, "product_url": "..."}]
"""
import logging
import time
import requests
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ar,en;q=0.9",
}


class BaseScraper(ABC):
    store_slug = None
    delay_between_requests = 2

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

    @abstractmethod
    def fetch_prices(self):
        """يُرجع قائمة بـ dicts: [{product_id, country_id, price, in_stock, product_url}]"""
        pass

    def get(self, url, **kwargs):
        time.sleep(self.delay_between_requests)
        try:
            r = self.session.get(url, timeout=15, **kwargs)
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            logger.error(f"[{self.store_slug}] خطأ في {url}: {e}")
            raise
