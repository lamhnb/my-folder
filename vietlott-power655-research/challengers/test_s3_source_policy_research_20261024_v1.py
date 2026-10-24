#!/usr/bin/env python3
"""Golden replay for S3 V1; requires pinned raw power655.jsonl as input."""
import argparse
import json
from pathlib import Path
from s3_source_policy_research_20261024_v1 import replay, predict_at, VERSION

ap = argparse.ArgumentParser()
ap.add_argument("--data", required=True)
args = ap.parse_args()
rows = [json.loads(line) for line in Path(args.data).read_text(encoding="utf-8").splitlines() if line.strip()]
assert len(rows) >= 1414 and rows[1413]["id"] == "01414"
result = replay(rows, first=789, last=1412)
expected = {"count": 624, "hits": 222, "quarters": [49, 52, 58, 63]}
assert result["totals"] == expected, (result["totals"], expected)
assert result["version"] == VERSION
assert len(result["records"]) == 624
if len(rows) >= 1415 and rows[1414]["id"] == "01415":
    case = predict_at(rows, 1414)
    assert case["momentum_top3"] == [52, 6, 3], case
    assert case["gap_long_top3"] == [15, 29, 44], case
print("S3 V1 golden PASS", result["totals"])
