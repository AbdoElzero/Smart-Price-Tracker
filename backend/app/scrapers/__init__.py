"""
نظام تسجيل الـ Scrapers.
لإضافة Scraper جديد، أضف كلاسه هنا.
"""

SCRAPERS = {
    # "store-slug": ScraperClass,
}


def get_scraper(store_slug):
    scraper_class = SCRAPERS.get(store_slug)
    return scraper_class() if scraper_class else None
