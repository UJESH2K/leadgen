from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Tender:
    source: str
    tender_id: str
    title: str
    organization: str
    state: Optional[str] = None
    city: Optional[str] = None
    category: Optional[str] = None
    tender_value_inr: Optional[float] = None
    published_at: Optional[datetime] = None
    closing_at: Optional[datetime] = None
    details_url: Optional[str] = None

    def to_dict(self) -> dict:
        payload = asdict(self)
        for key in ("published_at", "closing_at"):
            if payload[key] is not None:
                payload[key] = payload[key].isoformat()
        return payload


@dataclass
class Lead(Tender):
    score: float = 0.0
    reasons: list[str] = field(default_factory=list)
