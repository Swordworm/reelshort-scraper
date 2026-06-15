import json
from urllib.parse import urlparse, parse_qs, unquote
from reelshort.items import SeriesItem


def _decode_next_image(url: str) -> str:
    """Strip Next.js CDN wrapper: /_next/image?url=<encoded> → original URL."""
    if "/_next/image" in url:
        qs = parse_qs(urlparse(url).query)
        if "url" in qs:
            return unquote(qs["url"][0])
    return url


class ListingParser:
    def __init__(self, response):
        self.response = response
        self._data = self._load_next_data()

    def _load_next_data(self):
        raw = self.response.css("script#__NEXT_DATA__::text").get()
        if raw:
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                pass
        return None

    def get_items(self) -> list:
        if self._data:
            return self._items_from_json()
        return self._items_from_html()

    def _items_from_json(self) -> list:
        # TODO: adjust path once real JSON structure is known
        try:
            page_props = self._data["props"]["pageProps"]
            movies = (
                page_props.get("movieList")
                or page_props.get("movies")
                or page_props.get("data", {}).get("list")
                or []
            )
        except (KeyError, TypeError):
            movies = []

        items = []
        for m in movies:
            url = m.get("url") or m.get("slug") or m.get("id") or ""
            if url and not url.startswith("http"):
                url = "https://reelshort.com" + (url if url.startswith("/") else f"/movie/{url}")
            item = SeriesItem(
                series_url=url,
                series_title=m.get("title") or m.get("name") or "",
                cover_image_url=_decode_next_image(m.get("cover") or m.get("coverUrl") or m.get("img") or ""),
                description=m.get("description") or m.get("intro") or "",
                genre=m.get("genre") or m.get("category") or "",
            )
            items.append(item)
        return items

    def _items_from_html(self) -> list:
        items = []
        # TODO: tune selector after inspecting rendered HTML
        for card in self.response.css("a[href*='/movie/']"):
            href = card.attrib.get("href", "")
            if not href.startswith("http"):
                href = "https://reelshort.com" + href
            title = card.css("h2::text, h3::text, [class*='title']::text").get(default="").strip()
            img = card.css("img::attr(src), img::attr(data-src)").get(default="")
            item = SeriesItem(
                series_url=href,
                series_title=title,
                cover_image_url=_decode_next_image(img),
                description="",
                genre="",
            )
            items.append(item)
        return items

    def get_total_pages(self) -> int:
        if self._data:
            try:
                page_props = self._data["props"]["pageProps"]
                total = (
                    page_props.get("totalPage")
                    or page_props.get("total_pages")
                    or page_props.get("data", {}).get("totalPage")
                )
                if total:
                    return int(total)
            except (KeyError, TypeError, ValueError):
                pass

        # fallback: parse highest page number from pagination links
        nums = self.response.css("a[href*='/all-movies/']::attr(href)").getall()
        pages = []
        for href in nums:
            try:
                pages.append(int(href.rstrip("/").split("/")[-1]))
            except ValueError:
                pass
        return max(pages) if pages else 1
