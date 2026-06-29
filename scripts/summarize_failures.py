"""Summarize synthetic red-team failure logs."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize a JSON failure log.")
    parser.add_argument("failure_log", type=Path)
    args = parser.parse_args()

    failures = json.loads(args.failure_log.read_text(encoding="utf-8"))
    by_category = Counter(item["category"] for item in failures)
    by_severity = Counter(item["severity"] for item in failures)

    print("Failure summary")
    print("---------------")
    print(f"Total failures: {len(failures)}")
    print("\nBy category:")
    for category, count in sorted(by_category.items()):
        print(f"- {category}: {count}")
    print("\nBy severity:")
    for severity, count in sorted(by_severity.items()):
        print(f"- {severity}: {count}")
    print("\nTop recommendations:")
    for item in failures:
        print(f"- {item['test_id']}: {item['recommended_fix']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
