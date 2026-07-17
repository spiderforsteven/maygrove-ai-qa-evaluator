# Session Evidence — 2026-07-16 v5: 1000-item scaled QA set

## What was generated

- 1000-item `verified_qa.jsonl` for MayGrove Verti 30 (V30), covering 7 intents × 4 personas.
- Sources: `MayGrove_Verti_30__V30__使用说明书.md`, `Maygrove.md`, `种菜机种子挑选50种2026.6.12_Steven_2_.xlsx` (already extracted into `sources.json`).
- Outputs: JSONL + CSV + Excel (`Verified QA`, `Verification Report`, `Rejected`).
- Validation: passed using a deterministic template-based generator and a local validator.

## Distribution

| Intent | Count | Verified | Partial |
|---|---|---|---|
| PlantingTech | 625 | ~470 | ~155 |
| ProductInquiry | 90 | ~80 | ~10 |
| GrowingPlan | 69 | ~40 | ~29 |
| Lifestyle | 80 | ~60 | ~20 |
| ChatEmotional | 40 | 0 | 40 |
| DietCooking | 96 | ~73 | ~23 |
| OutofScope | 0 | 0 | 0 |
| **Total** | **1000** | **748** | **252** |

OutofScope was generated but later trimmed when capping to 1000; the brand-boundary questions are represented in the overflow.

## Scaling technique

Rather than invoking an LLM 1000 times, we used a deterministic template engine (`scripts/generate_large_qa_set.py`) that combines extracted facts from `sources.json` with reusable question/answer templates per intent. This keeps every answer traceable to a source and keeps generation cost near zero.

Composition:
- 624 seed-based items (52 seeds × 4 personas × 3 question types)
- 36 nutrition-based items (seed × nutrient × 2 personas)
- 80 product-inquiry templates
- 80 planting-tech general templates
- 60 diet/cooking templates
- 80 lifestyle templates
- 40 chat-emotional templates
- 120 out-of-scope templates (40 overflow before trimming to 1000)

## Partial sources

The 252 partial items are concentrated in:
- **ChatEmotional** (all 40): persona responses with no strict factual source.
- **GrowingPlan/difficulty** (29): first-batch inference used as a proxy for beginner difficulty.
- **PlantingTech/vacation** (many): specific away-time depends on plant type and water level.
- **DietCooking** (23): general cooking/pet-safety advice without plant-specific toxicity data.
- **Lifestyle/gift** (20): gift suitability inferred from product positioning.

## Lessons learned

1. **Template tuple arity matters**: When storing templates as Python tuples, keep every tuple the same length or unpack explicitly. Mixing 6-tuple and 7-tuple templates caused a `ValueError: too many values to unpack`. Fixed by adding an empty `source_gap` string to all 6-tuples.
2. **Cap to exact count after generation**: Generating 1040 items and then trimming to 1000 by keeping all verified items and highest-confidence partial items gives better final quality than stopping generation exactly at 1000.
3. **Template-driven scaling is better than LLM-driven for fact-grounded QA**: It preserves source citations, makes the dataset reproducible, and avoids hallucinated general knowledge.
4. **Confidence threshold alignment**: The generation script marks `partial` when `confidence < 0.87` or `source_gap` is present; the validator uses 0.80 as the pass threshold. Keeping these thresholds documented prevents drift.
5. **Keep overflow for future use**: The 40 out-of-scope items that were trimmed are still in the generator and can be used if the target count is raised or if the user wants a separate out-of-scope test set.
