import scrapy


class SeriesItem(scrapy.Item):
    series_url      = scrapy.Field()
    series_title    = scrapy.Field()
    cover_image_url = scrapy.Field()
    description     = scrapy.Field()
    genre           = scrapy.Field()
    episode_count   = scrapy.Field()
    status          = scrapy.Field()
    tags            = scrapy.Field()
