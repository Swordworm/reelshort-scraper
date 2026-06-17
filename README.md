# reelshort-scraper

Scrapy-based scraper for [ReelShort.com](https://www.reelshort.com) series catalog.

## Overview

Two-phase scrape:

1. **listing** spider — discovers all series URLs from paginated catalog, stores them in SQLite
2. **series** spider — scrapes detail page for each discovered series

Data is persisted to `reelshort.db` (SQLite) and exported to CSV.

## Setup

```bash
uv sync
```

## Usage

### 1. Collect series URLs

```bash
scrapy crawl listing
```

Scrapes all pages of `reelshort.com/movie-genres/all-movies/`. Deduplicates by `book_id` (stable hex ID in URL). Re-running is safe — existing rows are updated if URL slug changed.

### 2. Scrape series details

```bash
scrapy crawl series
```

Fetches detail page for every series where `scraped_at IS NULL`. Re-running retries any previously failed rows.

### 3. Export to CSV

```bash
scrapy exportcsv
```

Writes `reelshort_series.csv` with columns defined in `EXPORT_CSV_PATH` / `EXPORT_CSV_FIELDS` in `settings.py`.

## Database

SQLite file: `reelshort.db`. Created automatically on first run.

### `series` table — key columns

| Column | Description |
|---|---|
| `book_id` | Stable unique hex ID from URL (unique key) |
| `series_url` | Full URL — updated automatically if slug changes |
| `series_title` | Series name |
| `cover_image_url` | Cover image |
| `description` | Synopsis |
| `episode_count` | Total episodes |
| `tags` | Comma-separated genre/tag list |
| `book_genre` | Genre integer code |
| `book_type` | Type integer code |
| `book_source` | Source integer code |
| `update_status` | 1=ongoing, 2=completed |
| `read_count` | View count |
| `collect_count` | Bookmark count |
| `online_at` | Unix timestamp — went online |
| `publish_at` | Unix timestamp — published |
| `has_dub` | Boolean — dubbed audio available |
| `scraped_at` | UTC timestamp of last successful detail scrape |
| `exception` | Error message if detail scrape failed |

### `listing` table

Tracks per-page scrape state. One row per listing page URL.

## Settings

| Setting | Default | Description |
|---|---|---|
| `CONCURRENT_REQUESTS` | 16 | Parallel requests |
| `DOWNLOAD_DELAY` | 0.5s | Base delay between requests |
| `AUTOTHROTTLE_TARGET_CONCURRENCY` | 8.0 | Autothrottle target |
| `LOG_DIR` | `logs/` | Log file directory |
| `LOG_LEVEL` | `DEBUG` | Log verbosity |
| `EXPORT_CSV_PATH` | `reelshort_series.csv` | CSV output path |

## Possible improvements

- **Convergence loop** — listing spider misses series when site pagination reorders between concurrent requests. After all pages complete, compare `COUNT(DISTINCT book_id)` against `total_items` from the first page JSON; re-queue all pages if gap > 0. Repeat until counts match or a pass adds zero new rows. Use Scrapy's `spider_idle` signal to trigger re-queue without closing the spider.

- **Switch listing to `_next/data` JSON API** — ReelShort exposes `/_next/data/{buildId}/en/movie-genres/all-movies/{page}.json`. Extract `buildId` from first page `__NEXT_DATA__`, then request subsequent pages as JSON directly. Faster than HTML parsing and returns `book_id` natively — no URL extraction heuristic needed.

- **Populate metadata from listing** — the listing JSON already includes `book_title`, `book_pic`, `special_desc`, `chapter_count`, `tag`, `book_genre`, `book_type`, `book_source`, `read_count`, `collect_count`. Storing these during the listing phase reduces the work the series spider needs to do.

- **Remove `listing_id` FK from `Series`** — the relation is meaningless because series can appear on any page across runs due to unstable pagination order.
