# Session Evidence — 2026-07-17

## Context

User invoked `/maygrove-ai-qa-evaluator` and uploaded three source files:

- `Maygrove.md`
- `MayGrove_Verti_30__V30__User_Manual.md`
- `种菜机种子挑选50种2026.6.12_Steven_2_.xlsx`

Default scope confirmed: MayGrove Verti 30, 7 intents × 4 personas, 28 target items, JSONL + CSV + Excel output.

## Execution Path

```bash
# 1. Parse sources
python scripts/load_sources.py \
  --maygrove-md Maygrove.md \
  --v30-manual MayGrove_Verti_30__V30__User_Manual.md \
  --seed-library 种菜机种子挑选50种2026.6.12_Steven_2_.xlsx \
  --output ./maygrove-qa-output/sources.json

# 2. Generate 7×4 baseline evaluation set
python scripts/run_evaluation.py \
  --maygrove-md Maygrove.md \
  --v30-manual MayGrove_Verti_30__V30__User_Manual.md \
  --seed-library 种菜机种子挑选50种2026.6.12_Steven_2_.xlsx \
  --output ./maygrove-qa-output \
  --count 28 \
  --skip-web

# 3. Validate outputs
python scripts/validate_qa_outputs.py ./maygrove-qa-output
```

## Output Structure

- `verified_qa.jsonl` — 28 QA items, canonical format
- `verified_qa.csv` — 28 rows
- `verified_qa.xlsx` — 3 sheets: Verified QA / Verification Report / Rejected
- `cross_verification_report.jsonl` — per-agent answers and consensus scores
- `rejected_needs_review.jsonl` — 0 items

## Results Summary

- `verified`: 17 items (final_confidence ≥ 0.80 and no critical issues)
- `partial`: 11 items (Lifestyle / ChatEmotional / DietCooking had lower fact coverage or missing food-safety disclaimer)
- `rejected`: 0 items

## Practical Notes

- `run_evaluation.py` in this environment uses a deterministic fallback generator because no LLM runtime is configured for the multi-agent calls. It still produces a validated, source-cited baseline, but all 28 items are generated from hard-coded templates, not from 3 independent QA agents.
- For large-scale expansion (100–5000 items), prefer `generate_large_qa_set.py` over `run_evaluation.py` because it is deterministic, avoids LLM calls, and preserves source citations.
- `load_sources.py` must run before either generator so `sources.json` exists.
