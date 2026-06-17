import scrapy


class ListingItem(scrapy.Item):
    page_url = scrapy.Field()
    page_number = scrapy.Field()
    scraped_at = scrapy.Field()
    exception = scrapy.Field()
    series = scrapy.Field()  # list[str] of series URLs
