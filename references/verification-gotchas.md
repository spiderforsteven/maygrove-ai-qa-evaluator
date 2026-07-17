# Verification Gotchas for QA Evaluation Sets

Common pitfalls discovered while validating MayGrove QA outputs. Keep this reference handy when writing or debugging `scripts/validate_qa_outputs.py` and related evaluation-set generators.

## 1. Report files do not need the full QA schema

`cross_verification_report.jsonl` and `rejected_needs_review.jsonl` are auxiliary reports. They must be valid JSONL and must not duplicate IDs, but they do not need every field required by `verified_qa.jsonl`. Attempting to validate them with the same strict schema produces false-positive errors like:

```
line 1: missing fields ['confidence', 'facts', 'issues', 'reference_answer', ...]
```

**Fix**: in `validate_qa_outputs.py`, split the JSONL file list into strict and lenient:

```python
jsonl_files = [
    ("verified_qa.jsonl", True),
    ("cross_verification_report.jsonl", False),
    ("rejected_needs_review.jsonl", False),
]
for name, strict in jsonl_files:
    ...
    if strict:
        all_errors.extend(validate_record(record, line_no))
```

## 2. Confidence vs. verification_status must stay aligned

A `verified` item with `confidence < 0.80` is a contradiction. Choose a single threshold and apply it consistently in both the generation script and the validator. This skill uses 0.80 as the pass threshold.

## 3. source_gap must be non-empty when status is not "verified"

Algorithm engineers and human reviewers rely on `source_gap` to know what to fix. If `verification_status` is `partial` or `rejected`, always populate `source_gap` with a concise reason such as:

- "general cooking knowledge not in product docs"
- "user profile field not confirmed in requirements doc"
- "web source quality too low"

## 4. CSV and Excel headers must match the validator exactly

`validate_qa_outputs.py` checks `reader.fieldnames == CSV_COLUMNS`. If the generation script adds, removes, or reorders columns, validation fails. Update `CSV_COLUMNS` and the Excel writer together.

## 5. Excel row counts include the header

The validator prints `row_count` from `iter_rows()`, which includes the header row. A 50-item QA set will show 51 rows in `Verified QA` and 51 rows in `Verification Report`. This is expected; do not treat the extra row as a bug.

## 6. Facts need both text and source

Every fact object must contain `text` and `source`. If a QA item has no source citations, it should be `partial` or `rejected`, not `verified`.

## 7. Watch for percentage mis-attribution

When the source says "extends X by Y%", do not rewrite it as "reduces the opposite by Y%". Example: V30 Vacation mode extends the growth period by ~30%, not reduces water/energy use by ~30%. Keep the original dimension and wording.

## 8. Do not infer user profile fields

For GrowingPlan or any plan-recommendation question, only use profile inputs explicitly listed in the app requirements doc. If the doc does not mention "available light" as a user input, do not include it in the reference answer.

## 9. General knowledge in DietCooking / Lifestyle

Recipe steps, storage methods, and harvest-time nutrition claims are often general knowledge. They are acceptable for QA evaluation if:

- The answer is safe and plausible.
- The answer includes a disclaimer that it is general advice, not from the V30 manual.
- The item is tagged `partial` with a clear `source_gap`.

Do not mark recipe or storage answers as `verified` solely because they are common sense.

## 10. Empty rejected file is valid

A zero-record `rejected_needs_review.jsonl` is a valid success state. The validator should accept it without errors.

## Re-checklist before delivery

- [ ] `python scripts/validate_qa_outputs.py <output_dir>` exits 0
- [ ] `verified_qa.jsonl` has the expected number of records
- [ ] `verified` items all have `confidence >= 0.80` and non-empty `facts`
- [ ] `partial`/`rejected` items all have non-empty `source_gap`
- [ ] `verified_qa.csv` and `verified_qa.xlsx` headers match the validator
- [ ] Excel sheets are `Verified QA`, `Verification Report`, and `Rejected`
- [ ] No duplicate IDs across any JSONL file
- [ ] A sample critic pass (10 items × Critic A + Critic B/C) was run and fixes applied
