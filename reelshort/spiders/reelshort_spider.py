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
        total_pages = parser.get_total_pages()
        total_items = parser.get_total_items()
        self.logger.info("Total listing pages: %d, total items: %s", total_pages, total_items)

        yield from self._process_listing(parser)

        for page in range(2, total_pages + 1):
            yield scrapy.Request(self.start_url_template.format(page=page), callback=self.parse_listing)

    def parse_listing(self, response):
        yield from self._process_listing(ListingParser(response))

    def _process_listing(self, parser: ListingParser):
        scraped_urls = get_scraped_urls()
        stubs = parser.get_items()

        no_url = already_scraped = yielded = 0
        for stub in stubs:
            url = stub.get("series_url", "")
            if not url:
                no_url += 1
                continue
            if url in scraped_urls:
                already_scraped += 1
                continue
            yielded += 1
            yield scrapy.Request(url, callback=self.parse_detail, cb_kwargs={"stub": stub})

        self.logger.info(
            "%s: %d items — yielded=%d, no_url=%d, already_scraped=%d",
            parser.response.url, len(stubs), yielded, no_url, already_scraped,
        )

    def parse_detail(self, response, stub: SeriesItem):
        detail = DetailParser(response).get_item()
        yield SeriesItem(
            series_url=stub["series_url"],
            series_title=stub.get("series_title"),
            cover_image_url=stub.get("cover_image_url"),
            description=stub.get("description"),
            episode_count=detail.get("episode_count"),
            tags=detail.get("tags"),
            book_genre=detail.get("book_genre"),
            book_type=detail.get("book_type"),
            book_source=detail.get("book_source"),
            update_status=detail.get("update_status"),
            read_count=detail.get("read_count"),
            collect_count=detail.get("collect_count"),
            online_at=detail.get("online_at"),
            publish_at=detail.get("publish_at"),
            has_dub=detail.get("has_dub"),
        )
