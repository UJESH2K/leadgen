from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from leadgen_pipeline.scoring.ranker import rank_tenders
from leadgen_pipeline.sources.csv_drop import CsvDropSource
from leadgen_pipeline.sources.mock_cppt import MockCPPPSource


def load_profile(path: str = "config/business_profile.json") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run(days_ahead: int, min_score: float) -> int:
    profile = load_profile()
    sources = [MockCPPPSource(), CsvDropSource("data/in")]

    tenders = []
    for source in sources:
        tenders.extend(source.fetch())

    leads = rank_tenders(tenders, profile, days_ahead=days_ahead)
    leads = [l for l in leads if l.score >= min_score]

    out_dir = Path("data/out")
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = [l.to_dict() for l in leads]
    (out_dir / "leads.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    if payload:
        with open(out_dir / "leads.csv", "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=payload[0].keys())
            writer.writeheader()
            writer.writerows(payload)

    print(f"Generated {len(leads)} qualified leads")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Tender lead generation pipeline")
    sub = parser.add_subparsers(dest="command")

    run_cmd = sub.add_parser("run")
    run_cmd.add_argument("--days-ahead", type=int, default=30)
    run_cmd.add_argument("--min-score", type=float, default=0.4)

    args = parser.parse_args()
    if args.command == "run":
        return run(days_ahead=args.days_ahead, min_score=args.min_score)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
