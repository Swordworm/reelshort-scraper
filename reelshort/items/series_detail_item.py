import scrapy


class SeriesDetailItem(scrapy.Item):
    series_id = scrapy.Field()
    series_url = scrapy.Field()
    series_title = scrapy.Field()
    cover_image_url = scrapy.Field()
    description = scrapy.Field()
    episode_count = scrapy.Field()
    tags = scrapy.Field()
    book_genre = scrapy.Field()
    book_type = scrapy.Field()
    book_source = scrapy.Field()
    update_status = scrapy.Field()
    read_count = scrapy.Field()
    collect_count = scrapy.Field()
    online_at = scrapy.Field()
    publish_at = scrapy.Field()
    has_dub = scrapy.Field()
    exception = scrapy.Field()
