from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from leadgen_pipeline.models import Tender
from leadgen_pipeline.sources.base import TenderSource


class CsvDropSource(TenderSource):
    def __init__(self, folder: str = "data/in") -> None:
        self.folder = Path(folder)

    def fetch(self) -> list[Tender]:
        tenders: list[Tender] = []
        for file in self.folder.glob("*.csv"):
            with open(file, newline="", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    tenders.append(
                        Tender(
                            source=f"csv:{file.name}",
                            tender_id=row.get("tender_id", ""),
                            title=row.get("title", ""),
                            organization=row.get("organization", ""),
                            state=row.get("state") or None,
                            city=row.get("city") or None,
                            category=row.get("category") or None,
                            tender_value_inr=_to_float(row.get("tender_value_inr")),
                            published_at=_to_dt(row.get("published_at")),
                            closing_at=_to_dt(row.get("closing_at")),
                            details_url=row.get("details_url") or None,
                        )
                    )
        return tenders


def _to_float(v: str | None):
    if not v:
        return None
    return float(v)


def _to_dt(v: str | None):
    if not v:
        return None
    return datetime.fromisoformat(v)
