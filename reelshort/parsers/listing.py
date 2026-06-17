import json
import logging
from urllib.parse import urlparse, parse_qs, unquote

logger = logging.getLogger(__name__)


def _decode_next_image(url: str) -> str:
    if "/_next/image" in url:
        qs = parse_qs(urlparse(url).query)
        if "url" in qs:
            return unquote(qs["url"][0])
    return url


class ListingParser:
    BASE_URL = "https://www.reelshort.com"

    def __init__(self, response):
        self.response = response
        self._data = self._load_next_data()
        self._url_map = self._build_url_map()

    def _build_url_map(self) -> dict[str, str]:
        url_map = {}
        for href in self.response.css("a[href*='/movie/']::attr(href)").getall():
            book_id = href.rstrip("/").split("-")[-1]
            full = self.BASE_URL + href if not href.startswith("http") else href
            url_map[book_id] = full
        return url_map

    def _load_next_data(self):
        raw = self.response.css("script#__NEXT_DATA__::text").get()
        if raw:
            try:
                return json.loads(raw)
            except json.JSONDecodeError as e:
                logger.error("JSON decode failed on %s: %s", self.response.url, e)
        return None

    def get_items(self) -> list[str]:
        if self._data:
            return self._items_from_json()
        logger.warning("No __NEXT_DATA__ on %s, falling back to HTML", self.response.url)
        return self._items_from_html()

    def _items_from_json(self) -> list[str]:
        data = self._data
        if data is None:
            return []
        try:
            books = data["props"]["pageProps"]["tagBooks"]["books"]
        except (KeyError, TypeError):
            books = []

        urls = []
        missing = []
        for m in books:
            book_id = m.get("book_id") or m.get("_id", "")
            url = self._url_map.get(book_id, "")
            if not url:
                missing.append(book_id)
            else:
                urls.append(url)

        if missing:
            logger.warning(
                "%s: %d/%d items have no URL in HTML map (book_ids: %s)",
                self.response.url, len(missing), len(urls) + len(missing), missing,
            )
        return urls

    def _items_from_html(self) -> list[str]:
        urls = []
        for href in self.response.css("a[href*='/movie/']::attr(href)").getall():
            if not href.startswith("http"):
                href = self.BASE_URL + href
            urls.append(href)
        return urls

    def get_total_pages(self) -> int:
        if self._data:
            try:
                total = self._data["props"]["pageProps"]["totalPage"]
                if total:
                    return int(total)
            except (KeyError, TypeError, ValueError):
                pass

        nums = self.response.css("a[href*='/all-movies/']::attr(href)").getall()
        pages = []
        for href in nums:
            try:
                pages.append(int(href.rstrip("/").split("/")[-1]))
            except ValueError:
                pass
        return max(pages) if pages else 1

    def get_total_items(self) -> int | None:
        if self._data:
            try:
                return int(self._data["props"]["pageProps"]["tagBooks"]["total_items"])
            except (KeyError, TypeError, ValueError):
                pass
        return None
