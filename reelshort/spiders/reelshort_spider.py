import scrapy
from reelshort.items import SeriesItem
from reelshort.parsers.listing import ListingParser
from reelshort.parsers.detail import DetailParser
from reelshort.repository import get_scraped_urls


class ReelshortSpider(scrapy.Spider):
    name = "reelshort"
    allowed_domains = ["reelshort.com", "www.reelshort.com"]
    start_url_template = "https://www.reelshort.com/movie-genres/all-movies/{page}"

    async def start(self):
        yield scrapy.Request(self.start_url_template.format(page=1), callback=self.parse_first_listing)

    def parse_first_listing(self, response):
        parser = ListingParser(response)
        total = parser.get_total_pages()
        self.logger.info(f"Total listing pages: {total}")

        yield from self._process_listing(parser)

        for page in range(2, total + 1):
            yield scrapy.Request(self.start_url_template.format(page=page), callback=self.parse_listing)

    def parse_listing(self, response):
        yield from self._process_listing(ListingParser(response))

    def _process_listing(self, parser: ListingParser):
        scraped_urls = get_scraped_urls()

        for stub in parser.get_items():
            url = stub.get("series_url", "")
            if not url or url in scraped_urls:
                continue
            yield scrapy.Request(url, callback=self.parse_detail, cb_kwargs={"stub": stub})

    def parse_detail(self, response, stub: SeriesItem):
        detail = DetailParser(response).get_item()
        yield SeriesItem(
            series_url=stub.get("series_url", ""),
            series_title=stub.get("series_title", ""),
            cover_image_url=stub.get("cover_image_url", ""),
            description=stub.get("description", ""),
            genre=detail.get("genre") or stub.get("genre", ""),
            episode_count=detail.get("episode_count", ""),
            status=detail.get("status", ""),
            tags=detail.get("tags", ""),
        )
