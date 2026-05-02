from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from leadgen_pipeline.models import Lead, Tender


def rank_tenders(tenders: list[Tender], profile: dict[str, Any], days_ahead: int) -> list[Lead]:
    leads: list[Lead] = []
    now = datetime.now(timezone.utc)

    include_keywords = [k.lower() for k in profile.get("include_keywords", [])]
    exclude_keywords = [k.lower() for k in profile.get("exclude_keywords", [])]
    preferred_states = {s.lower() for s in profile.get("preferred_states", [])}

    for tender in tenders:
        score = 0.0
        reasons: list[str] = []
        title = tender.title.lower()

        if any(k in title for k in exclude_keywords):
            continue

        keyword_hits = sum(1 for k in include_keywords if k in title)
        if keyword_hits:
            score += min(0.5, 0.15 * keyword_hits)
            reasons.append(f"keyword_matches={keyword_hits}")

        if tender.state and tender.state.lower() in preferred_states:
            score += 0.2
            reasons.append("preferred_state")

        min_val = profile.get("min_tender_value_inr")
        max_val = profile.get("max_tender_value_inr")
        if tender.tender_value_inr is not None and min_val <= tender.tender_value_inr <= max_val:
            score += 0.2
            reasons.append("value_in_range")

        if tender.closing_at:
            closing = tender.closing_at
            if closing.tzinfo is None:
                closing = closing.replace(tzinfo=timezone.utc)
            days_left = (closing - now).days
            if 0 <= days_left <= days_ahead:
                score += 0.1
                reasons.append(f"closing_in_{days_left}_days")

        if score > 0:
            leads.append(Lead(**tender.__dict__, score=min(score, 1.0), reasons=reasons))

    return sorted(leads, key=lambda x: x.score, reverse=True)
