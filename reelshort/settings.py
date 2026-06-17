BOT_NAME = "reelshort"
SPIDER_MODULES = ["reelshort.spiders"]
NEWSPIDER_MODULE = "reelshort.spiders"

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 0.5
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 8.0

RETRY_TIMES = 2
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]
DOWNLOAD_TIMEOUT = 180

LOG_DIR = "logs"
LOG_LEVEL = "DEBUG"

COMMANDS_MODULE = "reelshort.commands"
EXTENSIONS = {"reelshort.extensions.FileLogging": 1}
ITEM_PIPELINES = {
    "reelshort.pipelines.listing_pipeline.ListingPipeline": 100,
    "reelshort.pipelines.series_pipeline.SeriesPipeline": 200,
}

EXPORT_CSV_PATH = "reelshort_series.csv"
EXPORT_CSV_FIELDS = [
    "series_title", "series_url", "cover_image_url", "description",
    "episode_count", "tags", "book_genre", "book_type", "book_source",
    "update_status", "read_count", "collect_count",
    "online_at", "publish_at", "has_dub",
]

DEFAULT_REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

FEED_EXPORT_ENCODING = "utf-8"
