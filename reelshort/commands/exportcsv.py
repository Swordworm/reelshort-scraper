import csv
from reelshort.base_export import BaseExportCommand


class Command(BaseExportCommand):

    def short_desc(self):
        return "Export scraped series to CSV"

    def export(self, rows: list, settings) -> None:
        fields = settings.getlist("EXPORT_CSV_FIELDS")
        path = settings.get("EXPORT_CSV_PATH")
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for row in rows:
                writer.writerow({f: getattr(row, f) or "" for f in fields})
        print(f"Exported {len(rows)} series → {path}")
