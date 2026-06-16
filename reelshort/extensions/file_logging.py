import logging
import os
from datetime import datetime


class FileLogging:
    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        log_dir = crawler.settings.get("LOG_DIR", "logs")
        os.makedirs(log_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = os.path.join(log_dir, f"scrape_{ts}.log")
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setFormatter(logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s"))
        log_level = getattr(logging, crawler.settings.get("LOG_LEVEL", "INFO"), logging.INFO)
        fh.setLevel(log_level)
        logging.root.addHandler(fh)
        crawler.spider_log_path = log_path
        return ext
