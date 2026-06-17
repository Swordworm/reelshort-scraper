import scrapy
from reelshort.spiders.reelshort_base_spider import ReelshortBaseSpider
from reelshort.parsers.detail import DetailParser
from reelshort.items import SeriesDetailItem
from reelshort.repository.series import get_unscraped_series


class SeriesReelshortSpider(ReelshortBaseSpider):
    name = "series"

    async def start(self):
        rows = get_unscraped_series()
        self.logger.info("Unscraped series to fetch: %d", len(rows))
        for series_id, url in rows:
            yield scrapy.Request(
                url,
                callback=self.parse_detail,
                errback=self.handle_error,
                cb_kwargs={"series_id": series_id},
                dont_filter=True,
            )

    def parse_detail(self, response, series_id: int):
        item = DetailParser(response).get_item()
        item["series_id"] = series_id
        yield item

    def handle_error(self, failure):
        series_id = failure.request.cb_kwargs.get("series_id")
        self.logger.error("Failed series_id=%s url=%s: %s", series_id, failure.request.url, failure)
        yield SeriesDetailItem(series_id=series_id, exception=str(failure))
