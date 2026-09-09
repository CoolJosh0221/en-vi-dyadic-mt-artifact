# Research artifact: Evaluating Pragmatic Appropriateness in English--Vietnamese Machine Translation with Dyadic Profiles

Zheng-Yu Huang and Richard Tzong-Han Tsai. WMT 2026.

This item-level-response-free artifact accompanies the paper.

## Included

- `data/source_requests.jsonl`: the 30 selected English workplace requests and
  their intended synthetic relationship profiles.
- `data/distinct_output_texts.jsonl`: 199 distinct
  source--Vietnamese-translation--displayed-context combinations recovered
  from the executed forms. Together these contain the textual content observed
  across all 210 selected generated-output records.
- `generation/generation_spec.json`: recorded systems, dates, parameters,
  retry policy, validation, and known missing execution fields.
- `generation/prompt_structure.md`: records-backed message-role and condition
  structure. This is not a substitute for the unavailable verbatim templates.
- `results/*.csv`: machine-readable aggregate and pseudonymous rater-specific
  summary tables reported in the paper.
- `analysis/verify_aggregates.py`: standard-library-only checks for inventory
  counts and the exact RQ1, RQ2, and post-hoc tests recoverable from aggregate
  sufficient statistics.
- `metadata/artifact_manifest.json`, `metadata/privacy_scan.json`, and
  `MANIFEST.sha256`: scope, privacy, and integrity records.

## Important output-table limitation

The executed forms contained 225 displayed main-task rows: 210 selected
generated outputs plus 15 hidden repeats. After removing all operational IDs,
schedule order, and exact duplicate content, 199 distinct
source/translation/context combinations remain. Eleven of the 210 selected
records share the same released fields as another selected record. The private
system/condition/output linkage map needed to expand those collisions into an
exact labeled 210-row table was not present in the release workspace, so this
artifact does not infer it. Consequently, this release supports inspection of
all distinct output text but not system-by-condition reconstruction at the
item level.

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

The exact templates/rendered prompts and full analysis scripts must be added
from the separately preserved generation/analysis packet before claiming full
generation or end-to-end result reproducibility.
