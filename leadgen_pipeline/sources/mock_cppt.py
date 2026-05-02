from __future__ import annotations

from datetime import datetime, timedelta

from leadgen_pipeline.models import Tender
from leadgen_pipeline.sources.base import TenderSource


class MockCPPPSource(TenderSource):
    """Local mock source to develop ranking logic before production scraping/API."""

    def fetch(self) -> list[Tender]:
        now = datetime.utcnow()
        return [
            Tender(
                source="mock_cppt",
                tender_id="2026_HEALTH_001",
                title="Supply of Paracetamol 500mg Tablets for district hospitals",
                organization="State Medical Procurement Corporation",
                state="Karnataka",
                category="Drugs",
                tender_value_inr=2_500_000,
                published_at=now - timedelta(days=2),
                closing_at=now + timedelta(days=12),
                details_url="https://example.gov/tenders/2026_HEALTH_001",
            ),
            Tender(
                source="mock_cppt",
                tender_id="2026_INFRA_010",
                title="Bridge rehabilitation package",
                organization="Public Works Department",
                state="Tamil Nadu",
                category="Civil Works",
                tender_value_inr=250_000_000,
                published_at=now - timedelta(days=1),
                closing_at=now + timedelta(days=6),
                details_url="https://example.gov/tenders/2026_INFRA_010",
            ),
        ]
