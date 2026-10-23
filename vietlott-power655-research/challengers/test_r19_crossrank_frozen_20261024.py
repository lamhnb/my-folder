#!/usr/bin/env python3
"""Golden replay tests for R19 Cross-ranking frozen experiment.

Run: python test_r19_crossrank_frozen_20261024.py path/to/power655.jsonl
Requires EXACT raw source artifact: git blob 1230696771274d48b261a0cfbd728444700c299e
Test result is valid only against this exact input and the two frozen source blobs.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from r19_crossrank_frozen_20261024 import replay

EXPECTED_BLOB = "1230696771274d48b261a0cfbd728444700c299e"
EXPECTED_SOURCE_BLOBS = {
    "r19_crossrank_frozen_20261024.py": "a7ebf4fa5216e1bfd4906087e04555044d3e58f0",
    "hybrid6_p3_r3.py": "252f6e0e3dad70a80a4b0cf7febe92d5d080e264",
}

def git_blob_hash(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def assert_blob(path, expected):
    actual = git_blob_hash(Path(path).read_bytes())
    assert actual == expected, (str(path), actual, expected)

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python test_r19_crossrank_frozen_20261024.py path/to/power655.jsonl")
    root = Path(__file__).resolve().parent
    for file, blob in EXPECTED_SOURCE_BLOBS.items():
        assert_blob(root / file, blob)
    data = Path(sys.argv[1])
    assert_blob(data, EXPECTED_BLOB)
    rows = [json.loads(x) for x in data.read_text(encoding="utf8").splitlines() if x.strip()]
    assert len(rows) == 1414
    assert rows[779]["id"] == "00944" and rows[779]["date"] == "2022-09-23"
    assert rows[779]["result"] == [1,12,21,28,30,44]
    assert rows[1413]["id"] == "01414"

    full = replay(rows, first=156)
    legacy = replay(rows, first=789, last=1412)
    for report, length, b, c in [
        (full, 1258, (4965,2166,[0,466,687,96,7,2,0]), (4925,2136,[2,488,667,93,6,1,1])),
        (legacy, 624, (2487,1084,[0,227,342,49,4,2,0]), (2473,1080,[0,233,335,50,4,1,1])),
    ]:
        assert report["draws"] == length
        for key, expected in [("baseline",b), ("crossrank",c)]:
            actual = report[key]
            assert (actual["coverage"],actual["best_hit_sum"],actual["histogram"]) == expected, (key, actual)

    cases = {r["id"]: r for r in full["records"]}
    jackpot = cases["01320"]
    assert jackpot["winning"] == [12,26,28,43,50,54]
    assert jackpot["baseline"]["best"] == 5 and jackpot["crossrank"]["best"] == 6
    assert jackpot["final"][4] == [12,26,28,43,50,54]
    assert [(s["ticket"],s["out"],s["in"]) for s in jackpot["swaps"]] == [
        (4,39,53), (3,33,46), (5,41,28)]
    assert sum(r["crossrank"]["best"] == 6 for r in full["records"]) == 1
    assert len(cases["01414"]["swaps"]) == 3
    print("PASS R19 frozen source blobs, dataset blob, 1258+624 summaries, #01320 golden ticket")

if __name__ == "__main__":
    main()
