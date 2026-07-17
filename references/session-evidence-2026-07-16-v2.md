# Session Evidence: MayGrove QA Evaluation v2.0

Date: 2026-07-16
Session goal: Upgrade `maygrove-ai-qa-evaluator` from a single-line pipeline to a 3×3×3 multi-agent pipeline and produce a 30-item verified evaluation set for algorithm engineers.

## Documents used

- `/home/hermeswebui/.hermes/webui/attachments/4512ec29fb99/MayGrove_Verti_30__V30__使用说明书.md` (V30 hardware manual)
- `/home/hermeswebui/.hermes/webui/attachments/4512ec29fb99/Maygrove.md` (App requirements/test cases)
- `/home/hermeswebui/.hermes/webui/attachments/4512ec29fb99/种菜机种子挑选50种2026.6.12_Steven_2_.xlsx` (50-variety seed library, added mid-session)

## Skill changes

- Rewrote `SKILL.md` to v2.0.0 with 3×3×3 multi-agent architecture (3 fact extractors, 3 QA generators, 3 critics, Cross-Verifier).
- Added 4 persona definitions in `references/persona-definitions.md`.
- Added 3×3×3 pipeline specification in `references/multi-agent-pipeline.md`.
- Added seed-library-to-intent mapping in `references/seed-library-source-mapping.md`.
- Added validation script `scripts/validate_qa_outputs.py` to check JSONL/CSV/Excel outputs before delivery.

## Generated outputs

Location: `/workspace/.hermes/plans/maygrove-eval-output/`

- `verified_qa.jsonl` — 30 verified Q&A pairs (canonical format)
- `verified_qa.csv` — 30 verified Q&A pairs (CSV format)
- `verified_qa.xlsx` — 3-sheet Excel: Verified QA, Verification Report, Rejected
- `cross_verification_report.jsonl` — 30 records with multi-agent answers and critic scores
- `rejected_needs_review.jsonl` — empty (all 30 passed verification)
- `README.md` — delivery notes and usage instructions

## Coverage

| Intent | Count | Notes |
|---|---|---|
| PlantingTech | 5 | Includes seed-library-specific variety facts (e.g., Romaine Cimmaron, climbing tomatoes) |
| ProductInquiry | 5 | Includes seed compatibility, first-batch seed kit, bottom-pod rules |
| GrowingPlan | 4 | Includes onboarding flow and first-batch variety recommendations |
| Lifestyle | 4 | Includes home placement, gifting, kid-friendly plants |
| ChatEmotional | 2 | Greeting and persona tone |
| DietCooking | 7 | Includes food-safety + pet-safety disclaimers and seed nutrition data |
| OutofScope | 3 | Financial, medical, and coding deflections |

Personas: Newbie 7, Busy Professional 8, Green Enthusiast 8, Troubleshooter 7.
Average verification confidence: 0.948.

## Key learnings

- The seed library Excel significantly improved PlantingTech and DietCooking QA quality by grounding answers in specific variety data.
- Parallel subagent generation per intent cluster (PlantingTech/ProductInquiry, GrowingPlan/Lifestyle/ChatEmotional, DietCooking/OutofScope) worked well and kept token usage bounded.
- Cross-verification in this run was a post-processing merge rather than truly independent LLM calls. A fully independent Cross-Verifier would be the next improvement.
- A validation script is necessary because subagents occasionally produce minor JSON syntax issues (e.g., extra quotes in `facts` items); catching these before delivery saves time.

## Next improvement ideas

- Add a true independent Cross-Verifier LLM call that does not see the original source documents.
- Add claim-level semantic matching between `reference_answer` and `facts` to compute fact coverage automatically.
- Generate a larger set (e.g., 100 pairs) by expanding the intent × persona matrix and adding more seed varieties.
- Add negative / adversarial examples where the expected answer is "I don't know" or "that depends on your environment."
