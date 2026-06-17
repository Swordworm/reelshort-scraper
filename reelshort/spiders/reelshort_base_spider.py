import scrapy


class ReelshortBaseSpider(scrapy.Spider):
    allowed_domains = ["reelshort.com", "www.reelshort.com"]
    BASE_URL = "https://www.reelshort.com"
    LISTING_URL = "https://www.reelshort.com/movie-genres/all-movies/{page}"
