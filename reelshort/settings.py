BOT_NAME = "reelshort"
SPIDER_MODULES = ["reelshort.spiders"]
NEWSPIDER_MODULE = "reelshort.spiders"

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1.0
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

COMMANDS_MODULE = "reelshort.commands"
ITEM_PIPELINES = {"reelshort.pipelines.SQLitePipeline": 300}

EXPORT_CSV_PATH = "reelshort_series.csv"
EXPORT_CSV_FIELDS = [
    "series_title", "series_url", "cover_image_url",
    "description", "genre", "episode_count", "status", "tags",
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
