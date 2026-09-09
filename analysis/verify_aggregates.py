#!/usr/bin/env python3
"""Recompute released exact tests from aggregate sufficient statistics."""

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows(name):
    with (ROOT / "results" / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def exact_two_sided_binomial(successes, failures):
    n = successes + failures
    if n == 0:
        return 1.0
    lower = min(successes, failures)
    tail = sum(math.comb(n, k) for k in range(lower + 1)) / (2 ** n)
    return min(1.0, 2.0 * tail)


def holm(raw):
    order = sorted(range(len(raw)), key=raw.__getitem__)
    adjusted = [0.0] * len(raw)
    running = 0.0
    m = len(raw)
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (m - rank) * raw[index]))
        adjusted[index] = running
    return adjusted


def close(actual, expected, tolerance=5e-4):
    if abs(actual - expected) > tolerance:
        raise AssertionError(f"{actual} != {expected} within {tolerance}")


def verify_rq1():
    data = rows("aggregate_rq1.csv")
    for row in data:
        p = exact_two_sided_binomial(int(row["improved"]), int(row["worsened"]))
        close(p, float(row["raw_p"]), 1e-8)
    for outcome in {row["outcome"] for row in data}:
        family = [row for row in data if row["outcome"] == outcome]
        adjusted = holm([float(row["raw_p"]) for row in family])
        for row, value in zip(family, adjusted):
            close(value, float(row["holm_p"]), 1e-8)


def verify_rq2():
    data = rows("aggregate_rq2.csv")
    raw = []
    for row in data:
        value = exact_two_sided_binomial(
            int(row["intended_only"]), int(row["reversed_only"])
        )
        close(value, float(row["raw_p"]), 5e-9)
        raw.append(value)
    for row, value in zip(data, holm(raw)):
        close(value, float(row["holm_p"]), 5e-9)


def verify_preference():
    data = rows("aggregate_preference.csv")
    raw = [
        exact_two_sided_binomial(int(row["dyad"]), int(row["base"]))
        for row in data
    ]
    adjusted = holm(raw)
    for row, value in zip(data, adjusted):
        reported = float(row["holm_p"])
        if reported == 0.0001:  # manuscript reports this cell as <.0001
            assert value < 0.0001
        else:
            close(value, reported, 5e-5)


def verify_inventory():
    source_count = sum(1 for _ in (ROOT / "data" / "source_requests.jsonl").open(encoding="utf-8"))
    text_count = sum(1 for _ in (ROOT / "data" / "distinct_output_texts.jsonl").open(encoding="utf-8"))
    assert source_count == 30, source_count
    assert text_count == 199, text_count


def main():
    verify_inventory()
    verify_rq1()
    verify_rq2()
    verify_preference()
    print("Artifact verification: PASS")
    print("  source requests: 30")
    print("  distinct released source/translation/context records: 199")
    print("  RQ1, RQ2, and post-hoc exact-test cells: verified")


if __name__ == "__main__":
    main()
