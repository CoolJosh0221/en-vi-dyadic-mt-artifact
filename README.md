# Research artifact: Evaluating Pragmatic Appropriateness in English–Vietnamese Machine Translation with Dyadic Profiles

Zheng-Yu Huang and Richard Tzong-Han Tsai. WMT 2026.

This item-level-response-free artifact accompanies the paper.

## Relation to the paper's Data Availability appendix

Appendix A of the paper describes an earlier version of this release and states
that the exact system/condition mapping and the verbatim prompt files are not
included. This release now includes them:

- `data/output_inventory.jsonl`: the system/condition label for each of the 210
  generated records;
- `generation/rendered_requests.jsonl` and `generation/prompt_templates.md`: the
  verbatim provider requests and prompt templates;
- `generation/attempt_log.csv`: the generation attempt archive.

These files describe machine-generated outputs and prompts only. They contain no
human judgments, so the human-data scope described in the paper is unchanged.

## Included

- `data/source_requests.jsonl`: the 30 selected English workplace requests and
  their intended synthetic relationship profiles.
- `data/distinct_output_texts.jsonl`: 199 distinct
  combinations of source text, Vietnamese translation, and displayed context, recovered
  from the executed forms. Together these contain the textual content observed
  across all 210 selected generated-output records.
- `data/output_inventory.jsonl`: the labeled 210-row inventory (see below).
- `generation/generation_spec.json`: recorded systems, dates, parameters,
  retry policy, validation, and known missing execution fields.
- `generation/rendered_requests.jsonl`, `generation/prompt_templates.md`,
  `generation/attempt_log.csv`: verbatim requests, templates, and attempt counts.
- `results/*.csv`: machine-readable aggregate and pseudonymous rater-specific
  summary tables reported in the paper.
- `analysis/verify_aggregates.py`: standard-library-only checks for the labeled
  inventory, prompt templates, the text-identity counts reported in Section 6.4,
  and the exact RQ1, RQ2, and post-hoc tests recoverable from aggregate
  sufficient statistics.
- `metadata/artifact_manifest.json`, `metadata/privacy_scan.json`, and
  `MANIFEST.sha256`: scope, privacy, and integrity records.

## Labeled output inventory

`data/output_inventory.jsonl` lists all 210 generated records with `release_source_id`
(`S01`–`S30`), `system` (Gemini, SEA-LION, Google Translate), `condition` (BASE, DYAD,
SWAPPED), the verbatim Vietnamese translation and its SHA-256, and
`release_text_record_id`, which joins each record to the 199
distinct source/translation/context rows in `data/distinct_output_texts.jsonl`
(eleven records share a row with another record because their released fields
coincide). `generation/rendered_requests.jsonl` holds the 210 provider request
bodies verbatim; `generation/prompt_templates.md` states the templates and
`generation/attempt_log.csv` the 241-request attempt archive (210 selected, 30
terminal errors, 1 interrupted).

With these files the system-by-condition structure of every table in the paper
can be inspected at the level of generated text. Human judgments remain
aggregate-only (see below), so the human-evaluation cells of Tables 3–8 are
verified from the released counts, not recomputed from item-level responses.

## Deliberately excluded

No item-level annotator response, free-text reason, adjudication rationale,
timestamp, schedule, participant or package identifier, agreement, payment
record, or join key is included. The primary annotators authorized
research-publication use under the pseudonymous A1 and A2 labels; public
release of item-level responses and free-text records is outside the documented
consent scope. The artifact includes only aggregate and pseudonymous
rater-specific summary cells already reported in the paper.

## Reproduce released checks

From the artifact root:

```bash
python3 analysis/verify_aggregates.py
shasum -a 256 -c MANIFEST.sha256
```

Generation is fully documented at the request level. End-to-end reproduction of
the human-evaluation tables from item-level judgments is not possible from this
release, by design.
