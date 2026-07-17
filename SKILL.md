---
name: maygrove-ai-qa-evaluator
description: "Generate fact-grounded Q&A evaluation datasets for the MayGrove AI assistant. Trigger: MayGrove QA evaluation, 7 intents, 正确率, hallucination, QA pairs, 算法工程师."
version: 2.0.1
author: "Hermes Agent"
---

# maygrove-ai-qa-evaluator

## When to use

- User asks to evaluate or benchmark MayGrove AI QA accuracy / 正确率.
- User asks to generate test questions and answers for the MayGrove assistant.
- User mentions: "评测", "正确率", "QA pairs", "7 大意图", "幻觉", "种植场景", "多视角", "算法工程师".
- User wants a dataset that can be handed directly to algorithm engineers for real-environment evaluation.

## Interaction Flow (IMPORTANT)

**Do not start generating the evaluation set until the user has provided or confirmed the required inputs.** This skill is fact-grounded; the quality of the output depends entirely on the sources. Always begin by asking the user for the materials below. If the user says "继续" / "OK" / "start", treat it as authorization to proceed **after** you have confirmed the inputs are available.

### Step 1: Intake — Ask the user for required materials

Use the following intake checklist. Ask the user to upload files or provide paths for each item. If an item is missing, note it as a `source_gap`.

| # | Required Input | Why it matters | Status |
|---|---|---|---|
| 1 | **Product overview / business context** | Understand what the product is, who the users are, and what the AI is supposed to do | Required |
| 2 | **AI assistant scope / intent categories** | What topics should the AI cover? (e.g., 7 intents for MayGrove) | Required |
| 3 | **User personas / target segments** | Whose questions are we simulating? | Required |
| 4 | **Product documentation / user manual** | Device specs, installation, maintenance, safety, troubleshooting | Strongly recommended |
| 5 | **App / software requirements** | Flows, entry points, copy rules, tone-of-voice, error messages | Strongly recommended |
| 6 | **Knowledge base / catalog / seed library** | Product-specific facts (varieties, SKUs, growth stages, nutrition, recipes) | Strongly recommended |
| 7 | **Brand boundary / Out-of-scope policy** | What the AI must refuse or deflect | Required |
| 8 | **Evaluation format preference** | JSONL primary + CSV/Excel + report? | Confirm |
| 9 | **Desired number of Q&A pairs** | Default 28 (7 intents × 4 personas) | Confirm |

### Step 2: Propose default assumptions based on MayGrove context

If the user has invoked this skill for MayGrove but has not provided files, propose the following defaults and ask for confirmation:

> "I can use the MayGrove default context: Verti 30 indoor garden, 7 intents (PlantingTech, ProductInquiry, GrowingPlan, Lifestyle, ChatEmotional, DietCooking, OutofScope), 4 personas (Newbie, Busy Professional, Green Enthusiast, Troubleshooter). Please provide or confirm the following files:
> 1. MayGrove product/app requirements doc (`Maygrove.md`)
> 2. V30 hardware user manual (`MayGrove_Verti_30__V30__使用说明书.md`)
> 3. Seed library Excel (`种菜机种子挑选50种2026.6.12_Steven_2_.xlsx`)
> 4. Any other brand-boundary or safety docs you want included."

### Step 3: Wait for user confirmation

- If user uploads files: proceed to source loading.
- If user says files are not needed / use defaults: proceed with the default MayGrove knowledge embedded in this skill, but explicitly mark `source_gap` for any claim that lacks a user-provided source.
- If user wants a different product: rewrite the intent/persona mapping together before generating.

### Step 4: Summarize understanding before execution

Before running the pipeline, output a concise confirmation like:

> "已确认评测范围：
> - 产品：MayGrove Verti 30
> - 7 大意图 + 4 人设
> - 来源：V30 说明书 + Maygrove.md + 50 种种子库
> - 输出：JSONL + CSV + Excel
> - 目标：30 条验证 Q&A
> 是否开始生成？"

Wait for user approval (e.g., "继续" / "OK" / "start") before generating.

See [references/intake-first-design-pattern.md](references/intake-first-design-pattern.md) for the reusable intake-first design pattern applied to any evaluation-skill scenario.

## Goal

Produce a **fact-grounded, multi-perspective-verified Q&A evaluation set** for the MayGrove AI assistant. Every generated answer must be traceable to a source (local documentation, seed library, or trusted web research). Multiple independent agents generate and verify from different angles, then a Cross-Verifier resolves conflicts. Low-confidence or under-sourced items are routed to manual review.

## 7 Intent Categories + 4 Personas

| Intent | Definition | Primary Sources | Seed Library Link |
|---|---|---|---|
| PlantingTech | Planting, watering, nutrients, light, seedlings, climbing, root management, pests | V30 manual §7–§15 + 种植Tips整理模版 | Germination/seedling/vegetative days per variety |
| ProductInquiry | Device specs, unboxing, installation, accessories, troubleshooting, app usage, seed compatibility | V30 manual + Maygrove.md | 是否爬藤、首批选种、自定义种子 |
| GrowingPlan | Onboarding plan flow, profile fields, entry points, plan actions, variety recommendations | Maygrove.md 种植规划 | 首批 10 种 + 30+2 容量组合 |
| Lifestyle | Home placement, gifting, growing with kids, community vibe | V30 manual intro + Maygrove.md + web research | 香草/花卉适合厨房/送礼 |
| ChatEmotional | Greetings, emotional support, persona tone, encouragement | Maygrove.md 日常招呼区 / 自由问答 | 非事实库，使用人设库 |
| DietCooking | Recipes, food safety, using harvests, nutrition | V30 manual safety tips + seed nutrition sheet + web research | 营养成分、收获后食用 |
| OutofScope | Topics unrelated to MayGrove, plants, or the app | Brand boundary definition | N/A |

**4 Personas:**
| Persona | Traits | Language style |
|---|---|---|
| **Newbie** | First day, zero experience | Simple, anxious, direct |
| **Busy Professional** | Time-poor, wants efficiency | Concise, schedule-focused, action-oriented |
| **Green Enthusiast** | Experienced, curious | Detailed, technical, comparative |
| **Troubleshooter** | Has a problem, needs fix | Symptom-specific, urgent, descriptive |

See [references/intent-source-mapping.md](references/intent-source-mapping.md) for detailed mapping.
See [references/persona-definitions.md](references/persona-definitions.md) for persona prompts.
See [references/seed-library-source-mapping.md](references/seed-library-source-mapping.md) for how the 50-variety seed database feeds into QA generation.
See [references/tavily-integration-notes.md](references/tavily-integration-notes.md) for Tavily setup.
See [references/multi-agent-pipeline.md](references/multi-agent-pipeline.md) for the 3×3×3 architecture.
See [references/intake-first-design-pattern.md](references/intake-first-design-pattern.md) for the general intake-first design pattern that applies to all evaluation-set skills.
See [references/verification-gotchas.md](references/verification-gotchas.md) for common validation pitfalls and how to fix them (e.g., report-file schema relaxation, confidence/status alignment, Excel header matching).
See [templates/fact_extractor_prompt.md](templates/fact_extractor_prompt.md), [templates/qa_generator_prompt.md](templates/qa_generator_prompt.md), [templates/critic_prompt.md](templates/critic_prompt.md), and [templates/cross_verifier_prompt.md](templates/cross_verifier_prompt.md) for reusable agent prompts.
See [scripts/run_evaluation.py](scripts/run_evaluation.py) to run the 7-intent × 4-persona baseline evaluation set (default 28 items).
See [scripts/generate_large_qa_set.py](scripts/generate_large_qa_set.py) for a deterministic, fact-grounded template generator that can produce 500–5000 PlantingTech-focused items from the extracted source JSON without LLM calls.
See [scripts/load_sources.py](scripts/load_sources.py) to parse the source documents into structured JSON.
See [scripts/validate_qa_outputs.py](scripts/validate_qa_outputs.py) to validate generated JSONL/CSV/Excel outputs before delivery.
See [references/session-evidence-2026-07-17.md](references/session-evidence-2026-07-17.md) for a concrete 28-item run and output structure.

## Quick Start

```bash
pip install -r scripts/requirements.txt

python scripts/run_evaluation.py \
  --maygrove-md /path/to/Maygrove.md \
  --v30-manual /path/to/MayGrove_Verti_30__V30__使用说明书.md \
  --seed-library /path/to/种菜机种子挑选50种2026.6.12_Steven_2_.xlsx \
  --output ./maygrove-qa-output \
  --count 30 \
  --skip-web

python scripts/validate_qa_outputs.py ./maygrove-qa-output
```

## Notes on the Implementation

- `run_evaluation.py` includes both a deterministic fallback generator and LLM-call hooks for the 3×3×3 agents. If no LLM CLI is configured, the fallback produces a validated dataset from the loaded sources so the pipeline is always runnable.
- `generate_large_qa_set.py` is a fully deterministic, template-driven generator for 500–5000 item sets. It is the preferred path when the user asks for large counts (e.g., 1000), because it preserves source citations and avoids LLM hallucination in general-knowledge areas. It expects `sources.json` produced by `load_sources.py`.
- The `data/` directory contains pre-extracted `seed_library_first_batch.json`, `seed_nutrition.json`, and `planting_tips.json` derived from the seed library Excel. These can be used for fast fact lookups without re-parsing the Excel file.
- If the user wants **more than 28 items**, expand by adding scenario variations per intent (e.g., water-level, vacation-mode, seedling-transplant) rather than duplicating the same 7×4 grid. The 50-item run on 2026-07-16 used this pattern successfully; see [references/session-evidence-2026-07-16-v4.md](references/session-evidence-2026-07-16-v4.md).
- For **1000+ item scales**, use a deterministic template engine seeded from the extracted source JSON. This preserves source citations and keeps generation cost near zero. See [references/session-evidence-2026-07-16-v5.md](references/session-evidence-2026-07-16-v5.md).
- After generating any fallback or LLM-based set, sample 10 items each with Critic A and Critic B/C subagents, then fix the flagged items before final validation. This catches wording mis-attributions (e.g., Vacation mode "30%") and unsupported general-knowledge claims in DietCooking.

## Multi-Agent Pipeline: 3 × 3 × 3 + Cross-Verifier

```
Local docs / Seed library / Web sources
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 1: 3 Independent Fact Extractors                 │
│  • FactAgent A — Strict literal extraction from docs     │
│  • FactAgent B — Cross-section inference/synthesis       │
│  • FactAgent C — External web research (Tavily)          │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  Consensus Check: CONSENSUS / MAJORITY / CONFLICT        │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 2: 3 Independent QA Generators                    │
│  • QAAgent A — Scenario-driven (user journey stages)     │
│  • QAAgent B — Fact-driven (reverse question from facts) │
│  • QAAgent C — Persona-driven (4 personas)               │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 3: 3 Independent Critics                          │
│  • Critic A — Fact traceability (every claim sourced)    │
│  • Critic B — Logical / physical plausibility            │
│  • Critic C — Safety & boundary compliance               │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  Cross-Verifier                                          │
│  • final_confidence = fact_coverage*0.3 + critic_avg*0.4 + consensus_score*0.3 │
│  • Passes only if ≥2 QA agents agree AND no critical issue │
└─────────────────────────────────────────────────────────┘
          │
          ▼
   verified_qa.jsonl / verified_qa.csv / verified_qa.xlsx
   cross_verification_report.jsonl
   rejected_needs_review.jsonl
```

### Layer 1: 3 Independent Fact Extractors

| Agent | Role | Output |
|---|---|---|
| **FactAgent A** | Literal extraction | Atomic facts, exact section citation, numbers preserved |
| **FactAgent B** | Synthesis & inference | Cross-section facts, annotated as `inferred` or `derived` |
| **FactAgent C** | Web research | Tavily-extracted facts with URL, only for gap topics |

**Consensus labels:**
- `CONSENSUS` — all 3 agree → confidence 0.95–1.0
- `MAJORITY` — 2 agree → confidence 0.80–0.94
- `CONFLICT` — all 3 differ → route to `rejected_needs_review.jsonl`
- `SINGLE_ONLY` — only 1 has it → route to `rejected_needs_review.jsonl` or lower confidence

### Layer 2: 3 Independent QA Generators

| Agent | Strategy | Example |
|---|---|---|
| **QAAgent A** | Scenario-driven | "Newbie, first day: What seeds should I start with?" |
| **QAAgent B** | Fact-driven | Given fact "Romaine Cimmaron harvests in 60–70 days", ask "How long does Romaine Cimmaron take?" |
| **QAAgent C** | Persona-driven | Generate the same question in Newbie, BusyPro, GreenEnthusiast, Troubleshooter voices |

### Layer 3: 3 Independent Critics

| Critic | Pass criteria | Fail criteria |
|---|---|---|
| **Critic A (Fact)** | Every claim has a source citation | Unsourced claim, mismatched number, wrong source |
| **Critic B (Logic)** | Causal chain is physically/biologically sound | Contradicts gardening常识, impossible sequence, over-promises |
| **Critic C (Safety)** | Includes required safety/boundary notes | Missing food-safety disclaimer, missing pet-toxicity note, answers OutofScope |

### Cross-Verifier

Combines all agent outputs into a single verdict:

```
final_confidence = (fact_coverage × 0.3) + (critic_avg × 0.4) + (consensus_score × 0.3)
```

- `consensus_score` = semantic similarity across the 3 QA answers (0.0–1.0)
- Pass threshold: `final_confidence >= 0.80` and `verification_status == verified`
- Otherwise: route to `rejected_needs_review.jsonl` with reason

## Output Formats

### 1. JSONL (Canonical — primary for algorithm engineers)

```json
{
  "id": "mg-001",
  "intent": "PlantingTech",
  "persona": "Newbie",
  "scenario": "first-day-setup",
  "question": "How long does Romaine Cimmaron lettuce take from seed to harvest?",
  "reference_answer": "Romaine Cimmaron lettuce is ready to harvest in about 60–70 days. The seed packet description notes it produces a 10–12 inch deep-red head with good flavor and crisp texture. (Source: 50-seed-library / Romaine Cimmaron)",
  "facts": [
    {"text": "Romaine Cimmaron is ready to harvest in 60–70 days", "source": "50-seed-library / Romaine Cimmaron / harvest/maturity"},
    {"text": "Produces a 10 to 12 inch, deep-red head with good flavor and crisp tender texture", "source": "50-seed-library / Romaine Cimmaron / description"}
  ],
  "confidence": 0.95,
  "tags": ["lettuce", "romaine-cimmaron", "harvest-time", "seed-library"],
  "verification_status": "verified",
  "verification_confidence": 0.95,
  "verification_notes": "All claims sourced from seed library. Numeric range preserved.",
  "issues": [],
  "source_gap": "无缺口",
  "agent_a_answer": "...",
  "agent_b_answer": "...",
  "agent_c_answer": "..."
}
```

### 2. CSV (Human review + quick filtering)

Columns: `id, intent, persona, scenario, question, reference_answer, facts_count, source_sections, confidence, verification_status, verification_confidence, source_gap, tags`

### 3. Excel (.xlsx)

Same as CSV but with:
- Filterable header row
- Separate sheet `verification_report` showing per-agent answers and consensus scores
- Separate sheet `rejected` showing low-confidence items

### 4. cross_verification_report.jsonl

Includes all 3 agent answers and all 3 critic scores for transparency and debugging.

### 5. rejected_needs_review.jsonl

Items with `verification_status != verified`, including the reason and the conflicting facts.

## Sources Used

1. **Local documents** (attached by user):
   - `Maygrove.md` — App requirements, flows, persona, copy rules
   - `MayGrove_Verti_30__V30__使用说明书.md` — Hardware manual
   - `种菜机种子挑选50种2026.6.12_Steven_2_.xlsx` — Seed library with 50 varieties, growth stages, nutrition
2. **Web research** (Tavily, only for gap topics): recipes, lifestyle advice, specific pest/disease facts
3. **Brand boundary policy** — for OutofScope deflection answers

## Execution Steps

### Phase 0: Intake & understanding confirmation

1. **Intake (ALWAYS RUN FIRST)**: Ask the user for the required materials using the intake checklist above. Do not proceed until inputs are confirmed or missing items are explicitly accepted as gaps.
2. **Understanding Summary**: Confirm product, intents, personas, sources, format, and target count with the user. Wait for approval before generating.

### Phase 1: Fact extraction

3. **Source Loading**: Split docs and seed Excel into chunks; preserve source path and section.
4. **Fact Extraction (3 agents)**: 
   - Spawn or prompt **FactAgent A** with `templates/fact_extractor_prompt.md` (role = literal extraction).
   - Spawn or prompt **FactAgent B** with `templates/fact_extractor_prompt.md` (role = cross-section synthesis).
   - If web research is enabled, spawn or prompt **FactAgent C** with `templates/fact_extractor_prompt.md` (role = Tavily web research).
   - Tag each fact with `CONSENSUS`, `MAJORITY`, `CONFLICT`, or `SINGLE_ONLY`.

### Phase 2: QA generation

5. **QA Generation (3 agents)**:
   - Spawn **QAAgent A** with `templates/qa_generator_prompt.md` (role = scenario-driven).
   - Spawn **QAAgent B** with `templates/qa_generator_prompt.md` (role = fact-driven).
   - Spawn **QAAgent C** with `templates/qa_generator_prompt.md` (role = persona-driven).
   - Each agent returns one candidate QA pair per (intent, persona) cell.

### Phase 3: Critic review

6. **Critic Review (3 agents)**:
   - Spawn **Critic A** with `templates/critic_prompt.md` (role = fact traceability).
   - Spawn **Critic B** with `templates/critic_prompt.md` (role = logical plausibility).
   - Spawn **Critic C** with `templates/critic_prompt.md` (role = safety & boundary).
   - Each critic returns a 0.0–1.0 score and issue list.

### Phase 4: Cross-verification & output

7. **Cross-Verification**: 
   - Spawn the **Cross-Verifier** with `templates/cross_verifier_prompt.md`.
   - Provide the 3 QA agent answers, the 3 critic scores, the consensus score, and the supporting facts.
   - The Cross-Verifier returns `verification_status`, `final_confidence`, and `issues`.
   - Keep items with `final_confidence >= 0.80` and no critical issue as `verified`.
   - Route conflicts, low-confidence items, and critical safety failures to `rejected_needs_review.jsonl`.
8. **Output**: Write `verified_qa.jsonl`, `verified_qa.csv`, `verified_qa.xlsx`, `cross_verification_report.jsonl`, `rejected_needs_review.jsonl`.
9. **Validation**: Run `python scripts/validate_qa_outputs.py /path/to/output/dir` on the output files. If validation fails, read the reported errors, fix the JSONL/CSV syntax or missing required fields, and re-run validation until it passes. Do not deliver files that fail validation.

## Failure Modes & Fallbacks

| Scenario | Trigger | Handling |
|---|---|---|
| No `TAVILY_API_KEY` | `tvly` search fails with auth error | Disable FactAgent C; mark web-dependent intents as `web_source_needed` and route to rejected. |
| `tvly` not installed | `tvly` command missing | Try `pip install tavily-cli`; if still missing, disable web research. |
| Seed library Excel missing | File not found at user-provided path | Generate QA without plant-specific variety facts; mark `source_gap`. |
| 3 QA agents conflict | Cross-Verifier detects no consensus | Route to `rejected_needs_review.jsonl` with conflict reason. |
| Missing safety disclaimer | Critic C flags DietCooking/PlantingTech answer | Regenerate with required V30 manual food-safety / pet-toxicity note. |
| OutofScope answered incorrectly | Critic C flags non-deflection answer | Rewrite answer as deflection; do not answer the off-topic question. |
| User refuses intake / provides no sources | User says "不需要材料" or skips checklist | Output a warning: "Without sources, I can only generate speculative QA with high source_gap. Do you want to proceed?" If yes, mark all items as `source_gap` and lower confidence. |
| User wants a different product | Not MayGrove | Restart intake: ask for product name, intents, personas, sources, and brand boundary. Do not use MayGrove defaults. |
### Output validation fails | `scripts/validate_qa_outputs.py` returns errors | Fix JSONL/CSV syntax or missing required fields, then re-run validation. If errors are on `cross_verification_report.jsonl` or `rejected_needs_review.jsonl`, only those two files need JSON validity and ID uniqueness; relax the strict full-schema check for report files (see script implementation). |
| LLM auto-detection only works with Hermes CLI, OpenAI-compatible API, or Anthropic API | No API key or Hermes CLI available | The script prints a message and falls back to deterministic template generation. No additional setup needed. |
| openai/anthropic package missing when using direct API | `ModuleNotFoundError` | `pip install openai anthropic` — these are optional dependencies; the script gracefully falls back to templates if the import fails. |
| Web research returns low-quality sources | Tavily results are forums, e-commerce, or video-only | Reject web facts; mark as `source_gap` and route to rejected. |
| Generated QA exceeds desired count | More than user-specified N | Sort by final_confidence descending and keep top N; move overflow to a separate overflow file. For deterministic template engines, generate a small buffer (e.g., 4% extra) then trim to exact count while keeping all verified items first. See [references/session-evidence-2026-07-16-v5.md](references/session-evidence-2026-07-16-v5.md). |
| Template arity mismatch | Mixing 6-tuple and 7-tuple templates with `for q, a, ... in templates` | Ensure all template tuples have the same length; add an empty string for optional `source_gap` rather than omitting it. |

### How to handle "继续" / "OK" without prior intake

If the user says "继续" or "OK" before the intake checklist is complete, do **not** treat it as authorization to generate. Instead, output:

> "I need to confirm the required materials before proceeding. Please upload or provide paths for: [checklist]. If you want to use MayGrove defaults, say 'use MayGrove defaults'."

Only after the user explicitly confirms the checklist (or selects defaults) may generation begin.

## Anti-Patterns

- Do not generate questions that require information not present in the provided sources.
- Do not invent recipes, nutritional claims, or health benefits without a web source.
- Do not answer OutofScope questions; always deflect back to MayGrove/planting topics.
- Do not ignore the V30 manual's food-safety and pet-toxicity warnings.
- Do not claim exact harvest dates per plant unless the seed library or manual supports it.
- Do not use price, purchase links, or brand comparisons from web sources.
- Do not attribute a percentage change to the wrong dimension (e.g., V30 Vacation mode extends the growth period by ~30%, not reduces water/energy use by ~30%).
- Do not infer user profile fields for GrowingPlan unless `Maygrove.md` or the app requirements doc explicitly supports them.
- **Do not skip the intake step; even if the user says "继续" or "OK", confirm the required materials exist before generating.**
- **Do not assume the default MayGrove context if the user is asking about a different product.**
