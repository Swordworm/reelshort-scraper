import scrapy
from datetime import datetime, timezone
from reelshort.spiders.reelshort_base_spider import ReelshortBaseSpider
from reelshort.parsers.listing import ListingParser
from reelshort.items import ListingItem


class ListingReelshortSpider(ReelshortBaseSpider):
    name = "listing"

    async def start(self):
        yield scrapy.Request(self.LISTING_URL.format(page=1), callback=self.parse_first_listing)

    def parse_first_listing(self, response):
        parser = ListingParser(response)
        total_pages = parser.get_total_pages()
        total_items = parser.get_total_items()
        self.logger.info("Total pages: %d, total items: %s", total_pages, total_items)

        yield self._make_listing_item(response.url, 1, parser)

        for page in range(2, total_pages + 1):
            yield scrapy.Request(
                self.LISTING_URL.format(page=page),
                callback=self.parse_listing,
            )

    def parse_listing(self, response):
        try:
            page_num = int(response.url.rstrip("/").split("/")[-1])
        except ValueError:
            page_num = 0
        parser = ListingParser(response)
        yield self._make_listing_item(response.url, page_num, parser)

    def _make_listing_item(self, url: str, page_num: int, parser: ListingParser) -> ListingItem:
        series_urls = parser.get_items()
        self.logger.info("%s: %d series URLs found", url, len(series_urls))
        return ListingItem(
            page_url=url,
            page_number=page_num,
            scraped_at=datetime.now(timezone.utc),
            exception=None,
            series=series_urls,
        )
