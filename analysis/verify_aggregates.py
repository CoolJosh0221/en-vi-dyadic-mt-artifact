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



def _jsonl(name):
    import json
    with (ROOT / "data" / name).open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def verify_labeled_inventory():
    import hashlib, json as _json, unicodedata
    from collections import Counter
    nfc = lambda s: unicodedata.normalize("NFC", s).strip()
    inventory = _jsonl("output_inventory.jsonl")
    sources = {s["release_source_id"]: s for s in _jsonl("source_requests.jsonl")}
    texts = {t["release_text_record_id"]: t for t in _jsonl("distinct_output_texts.jsonl")}
    with (ROOT / "generation" / "rendered_requests.jsonl").open(encoding="utf-8") as handle:
        rendered = {r["record_id"]: r for r in (_json.loads(l) for l in handle if l.strip())}

    assert len(inventory) == 210, len(inventory)
    counts = Counter((r["system"], r["condition"]) for r in inventory)
    assert counts == Counter({("Gemini", "BASE"): 30, ("Gemini", "DYAD"): 30, ("Gemini", "SWAPPED"): 30, ("SEA-LION", "BASE"): 30, ("SEA-LION", "DYAD"): 30, ("SEA-LION", "SWAPPED"): 30, ("Google Translate", "BASE"): 30}), counts
    assert len({r["release_text_record_id"] for r in inventory}) == 199
    for r in inventory:
        assert hashlib.sha256(r["vietnamese_translation"].encode("utf-8")).hexdigest() == r["translation_sha256"], r["record_id"]
        assert texts[r["release_text_record_id"]]["vietnamese_translation"] == r["vietnamese_translation"], r["record_id"]
        assert texts[r["release_text_record_id"]]["release_source_id"] == r["release_source_id"], r["record_id"]

    gemini_base = "Translate the following English sentence into Vietnamese. Output only the translation, nothing else.\n\n"
    gemini_head = "Translate the following English sentence into Vietnamese.\nSocial context:\n- Speaker profile: "
    gemini_tail = "\nOutput only the translation, nothing else.\n\n"
    sealion_base = "You are a professional translator. Translate the user message from English to Vietnamese. Output only the Vietnamese translation, nothing else."
    sealion_head = "You are a professional translator. Translate the user message from English to Vietnamese.\nSocial context:\n- Speaker profile: "
    sealion_tail = "\nOutput only the Vietnamese translation, nothing else."
    for r in inventory:
        req = rendered[r["record_id"]]["request"]
        source = sources[r["release_source_id"]]
        english = source["english_source"]
        if r["system"] == "Gemini":
            user = req["request_body"]["contents"][0]["parts"][0]["text"]
            if r["condition"] == "BASE":
                assert user == gemini_base + english, r["record_id"]
            else:
                assert user.startswith(gemini_head) and user.endswith(gemini_tail + english), r["record_id"]
        elif r["system"] == "SEA-LION":
            messages = req["request_body"]["messages"]
            assert messages[-1]["content"] == english, r["record_id"]
            if r["condition"] == "BASE":
                assert messages[0]["content"] == sealion_base, r["record_id"]
            else:
                assert messages[0]["content"].startswith(sealion_head) and messages[0]["content"].endswith(sealion_tail), r["record_id"]
        else:
            assert req["text"] == english and r["condition"] == "BASE", r["record_id"]
        if r["condition"] in ("DYAD", "SWAPPED"):
            block = user if r["system"] == "Gemini" else messages[0]["content"]
            speaker = source["sender_profile"]["role"] if r["condition"] == "DYAD" else source["recipient_profile"]["role"]
            assert block.startswith((gemini_head if r["system"] == "Gemini" else sealion_head) + "role=" + speaker + ";"), r["record_id"]

    text = {(r["system"], r["condition"], r["release_source_id"]): nfc(r["vietnamese_translation"]) for r in inventory}
    direction = {sid: s["relationship"]["relationship_direction"] for sid, s in sources.items()}
    hier = [s for s, d in direction.items() if d in ("↑", "↓")]
    peer = [s for s, d in direction.items() if d == "↔"]
    assert len(hier) == 20 and len(peer) == 10
    def differ(system, a, b, ids):
        return sum(text[(system, a, s)] != text[(system, b, s)] for s in ids)
    assert differ("Gemini", "BASE", "DYAD", sources) == 30
    assert differ("SEA-LION", "BASE", "DYAD", sources) == 28
    assert differ("Gemini", "DYAD", "SWAPPED", hier) == 20 and differ("SEA-LION", "DYAD", "SWAPPED", hier) == 20
    assert differ("Gemini", "DYAD", "SWAPPED", peer) == 6 and differ("SEA-LION", "DYAD", "SWAPPED", peer) == 4
    ties = [s for s in sources if text[("SEA-LION", "BASE", s)] == text[("SEA-LION", "DYAD", s)]]
    assert len(ties) == 2 and all(direction[s] == "↔" for s in ties), ties


def main():
    verify_inventory()
    verify_labeled_inventory()
    verify_rq1()
    verify_rq2()
    verify_preference()
    print("Artifact verification: PASS")
    print("  source requests: 30")
    print("  distinct released source/translation/context records: 199")
    print("  labeled output inventory: 210 (90/90/30), templates and Section 6.4 identity counts: verified")
    print("  RQ1, RQ2, and post-hoc exact-test cells: verified")


if __name__ == "__main__":
    main()
