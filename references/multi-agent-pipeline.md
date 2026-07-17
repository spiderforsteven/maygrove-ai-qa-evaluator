# MayGrove AI QA: 3×3×3 Multi-Agent Pipeline

This document describes the multi-agent pipeline used to generate low-hallucination Q&A evaluation sets for the MayGrove AI assistant.

## Why Multi-View?

A single LLM pipeline can drift into plausible-sounding but unsupported answers. By running **independent agents from different angles** and requiring agreement before acceptance, we make hallucination structurally harder.

## Pipeline Overview

```
INPUT: Local docs + seed library + optional web
            │
            ▼
┌────────────────────────────────────────────┐
│  LAYER 1: Fact Extraction (3 agents)       │
│  • A: Literal extraction                   │
│  • B: Cross-section synthesis              │
│  • C: Web research (Tavily, optional)      │
└────────────────────────────────────────────┘
            │
            ▼
        Consensus Labeling
            │
            ▼
┌────────────────────────────────────────────┐
│  LAYER 2: QA Generation (3 agents)         │
│  • A: Scenario-driven user journey          │
│  • B: Fact-driven reverse question          │
│  • C: Persona-driven 4 voices               │
└────────────────────────────────────────────┘
            │
            ▼
┌────────────────────────────────────────────┐
│  LAYER 3: Critic Review (3 agents)          │
│  • A: Fact traceability                     │
│  • B: Logical plausibility                  │
│  • C: Safety & boundary compliance           │
└────────────────────────────────────────────┘
            │
            ▼
┌────────────────────────────────────────────┐
│  Cross-Verifier                             │
│  • Merges 3 QA answers + 3 critic scores    │
│  • Passes only if confidence >= 0.80       │
│  • Routes conflicts to rejected             │
└────────────────────────────────────────────┘
            │
            ▼
   verified_qa.jsonl / .csv / .xlsx
```

## Layer 1: Fact Extraction

### FactAgent A — Literal Extractor

**Mission:** Read the provided documents word-for-word and emit atomic facts with exact section citations.

**Rules:**
- One fact per sentence.
- Preserve numbers, units, and ranges exactly as written.
- Cite `source_file` and `source_section`.
- Do not paraphrase unless necessary for clarity.

**Example output:**
```json
{"text": "V30 tank capacity is about 26.5L (7gal).", "source": "V30 manual / 17 规格参数 / 整机规格", "type": "direct", "agent": "A"}
```

### FactAgent B — Synthesis Extractor

**Mission:** Cross-reference sections and infer derived facts, explicitly labeling them as `direct` or `inferred`.

**Rules:**
- Only infer when the conclusion is logically forced by multiple direct facts.
- Mark inferred facts with `inferred: true` and list the supporting facts.
- Never infer outside the document scope.

**Example output:**
```json
{"text": "Because V30 has 30 standard pods + 12 seedling slots and the manual recommends 20% minimum water at startup, a full plan should account for both capacity and initial water level.", "source": "V30 manual / 4 开箱清单 + 7 快速开始 / 第二步", "inferred": true, "agent": "B"}
```

### FactAgent C — Web Researcher (Optional)

**Mission:** Fill knowledge gaps for topics not well-covered by local docs (recipes, lifestyle plant lists, specific pest advice).

**Rules:**
- Use Tavily search + extract only if `TAVILY_API_KEY` is set and `tvly` is installed.
- Prefer authoritative domains: extension.org, thespruce.com, costafarms.com, seriouseats.com, loveandlemons.com.
- Block e-commerce, forums, and video-only pages.
- Cite exact URL.
- If Tavily is unavailable, disable this agent and continue with A and B only.

**Example output:**
```json
{"text": "A simple cherry tomato salad uses cherry tomatoes, parsley, lemon juice, olive oil, salt, pepper, and garlic.", "source": "https://onepotrecipes.com/cherry-tomato-salad-recipe", "type": "web", "agent": "C"}
```

### Consensus Check

After all 3 agents run, compare facts by semantic similarity (same topic + same numeric claim):

| Label | Condition | Confidence |
|---|---|---|
| `CONSENSUS` | All 3 agents produce equivalent fact | 0.95–1.00 |
| `MAJORITY` | 2 agents produce equivalent fact | 0.80–0.94 |
| `CONFLICT` | 3 agents disagree on a material claim | route to rejected |
| `SINGLE_ONLY` | Only 1 agent has the fact | route to rejected |

## Layer 2: QA Generation

### QAAgent A — Scenario-Driven

**User journey stages:**
1. **First-day setup** — unboxing, where to place, what seeds to start
2. **Daily care** — watering, light, nutrients, observation
3. **Troubleshooting** — pump failure, yellow leaves, pests, alarms
4. **Harvest & cooking** — when to harvest, recipes, nutrition
5. **Vacation / absence** — auto-refill, vacation mode, long trips

**Instruction:** Generate one natural question per (intent, persona, stage) combination. Ensure the question sounds like a real user at that moment.

### QAAgent B — Fact-Driven

**Instruction:** For each fact in the consensus fact pool, generate one question whose answer uses that fact. Ensure the question is answerable from the fact alone.

**Example:**
- Fact: "Romaine Cimmaron harvests in 60–70 days"
- Question: "How long does Romaine Cimmaron lettuce take from seed to harvest?"

### QAAgent C — Persona-Driven

**Instruction:** Take the same underlying fact and rephrase it in the voice of each of the 4 personas. Capture differences in vocabulary, urgency, and detail level.

**Example for "tank cleaning frequency":**
- **Newbie:** "Do I need to clean the tank? How often?"
- **Busy Professional:** "Can you put tank cleaning on my calendar so I don't forget?"
- **Green Enthusiast:** "What's the recommended maintenance schedule for the reservoir?"
- **Troubleshooter:** "My water looks cloudy. How often should I clean the tank to prevent this?"

## Layer 3: Critic Review

### Critic A — Fact Traceability

**Checklist:**
- [ ] Every sentence in `reference_answer` has a corresponding fact in `facts`.
- [ ] Numbers and units match exactly (or are clearly paraphrased with the same meaning).
- [ ] No source is invented or misattributed.

**Score:** 0.0–1.0

### Critic B — Logical Plausibility

**Checklist:**
- [ ] Causal claims are physically/biologically reasonable.
- [ ] Sequence of steps is correct and safe.
- [ ] No over-promising (e.g., "guaranteed harvest in 30 days").

**Score:** 0.0–1.0

### Critic C — Safety & Boundary Compliance

**Checklist:**
- [ ] Food-safety disclaimer included for edible plants (V30 manual §15.12).
- [ ] Pet-toxicity warning included when relevant.
- [ ] OutofScope questions are deflected, not answered.
- [ ] No PII, medical, financial, or legal advice.

**Score:** 0.0–1.0

## Cross-Verifier

### Inputs
- 3 generated answers from Layer 2
- 3 critic scores from Layer 3
- Fact coverage ratio (fraction of answer claims with sources)
- Consensus similarity score across the 3 answers

### Formula

```
fact_coverage = (sourced_claims) / (total_claims)
critic_avg = (critic_A + critic_B + critic_C) / 3
consensus_score = semantic_similarity(agent_a_answer, agent_b_answer, agent_c_answer)

final_confidence = (fact_coverage × 0.30) + (critic_avg × 0.40) + (consensus_score × 0.30)
```

### Verdict
- If `final_confidence >= 0.80` and no critical issue: `verification_status = verified`
- Else: `verification_status = partial` or `rejected`, with reason in `verification_notes`

### Output Routing

| Status | Destination | Use |
|---|---|---|
| `verified` | `verified_qa.jsonl` / `.csv` / `.xlsx` | Algorithm evaluation |
| `partial` | `verified_qa.jsonl` with flag | Manual spot-check before use |
| `rejected` | `rejected_needs_review.jsonl` | Human review, difficult cases |

## Execution Notes

- Agents do not see each other's outputs until the Cross-Verifier stage.
- All agents are instructed to output only what is supported by sources.
- Web research is optional; if disabled, the pipeline still runs with FactAgents A and B only.
- The Cross-Verifier is itself a separate LLM call with no access to original sources, only to the agent outputs and facts.
- Invoke the pipeline with: `python scripts/run_evaluation.py --maygrove-md PATH --v30-manual PATH --seed-library PATH --output PATH --count N [--skip-web]`.
