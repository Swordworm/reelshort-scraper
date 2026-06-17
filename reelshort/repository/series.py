from sqlalchemy import select
from reelshort.database import get_session
from reelshort.models import Series


def get_unscraped_series() -> list[tuple[int, str]]:
    with get_session() as session:
        rows = session.execute(
            select(Series.id, Series.series_url).where(Series.scraped_at.is_(None))
        ).all()
        return [(row.id, row.series_url) for row in rows]
