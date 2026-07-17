# Intake-First Design Pattern for Evaluation Skills

This pattern applies to any skill whose job is to generate a **fact-grounded evaluation set** (Q&A pairs, test cases, benchmark datasets) for an AI assistant or product feature. The core rule is: **do not generate until the required sources are confirmed.**

## Why intake-first matters

Evaluation datasets are only as good as the facts behind them. If the skill starts generating before it has the product context, the result is either:

- Hallucinated facts masquerading as ground truth
- Generic questions that do not match the real product
- Safety/boundary claims without source support

An intake step forces the user to supply (or confirm) the materials that become the ground truth.

## When to use this pattern

Use this pattern when the skill is asked to:

- Generate Q&A pairs for correctness evaluation
- Build test sets for AI assistant benchmarking
- Create reference answers for human or automated evaluation
- Produce any dataset where factual accuracy matters

## The 9-item intake checklist

| # | Input | Why it matters | If missing |
|---|---|---|---|
| 1 | Product overview / business context | Anchor the evaluation in the right domain | Ask the user for a one-sentence description |
| 2 | AI assistant scope / intent categories | Define what the assistant should cover | Propose a default taxonomy and ask for confirmation |
| 3 | User personas / target segments | Shape realistic questions | Propose 3–4 default personas |
| 4 | Product documentation / manual | Source for specs, installation, safety, troubleshooting | Mark `source_gap` for unsupported claims |
| 5 | App / software requirements | Source for flows, entry points, copy rules | Mark `source_gap` |
| 6 | Knowledge base / catalog / seed library | Source for product-specific facts | Mark `source_gap` |
| 7 | Brand boundary / out-of-scope policy | Required for deflection/refusal questions | Use a conservative default and ask for confirmation |
| 8 | Output format preference | JSONL, CSV, Excel, YAML, etc. | Default to JSONL + CSV + Excel |
| 9 | Desired number of items | Controls scope and cost | Default to 7 intents × 4 personas = 28 |

## How to handle premature "continue" / "OK" / "start"

Users often say "continue" before providing materials. This is **not** authorization to skip intake. Respond with:

> "I need to confirm the required materials before generating. Please upload or provide paths for: [list missing items]. If you want to use the default context, say 'use defaults'."

Only begin generation after one of:

- The user uploads/provides all required materials
- The user explicitly says "use defaults" or "use MayGrove defaults"
- The user explicitly accepts missing items as `source_gap`

## Handling different products

If the user is not evaluating MayGrove, do **not** reuse the MayGrove default context. Instead, restart intake with the product name and ask for:

- Product name and one-line description
- Intent taxonomy (propose a generic starter set if helpful)
- Personas (propose a generic starter set)
- Sources
- Brand boundary

Then generate the evaluation set using the same multi-agent pipeline.

## Embedding this pattern in a skill

1. Put the intake checklist near the top of `SKILL.md`, right after the trigger conditions.
2. Add a "How to handle continue/OK without prior intake" subsection in Failure Modes.
3. Add an anti-pattern: "Do not skip intake even if the user says continue."
4. Provide default assumptions only as a fallback, clearly labeled.

## Anti-patterns

- **Generate first, ask questions later** — produces low-quality, ungrounded outputs.
- **Assume the default product context** — wrong product leads to wrong evaluation.
- **Treat "continue" as blanket authorization** — disables the safety gate that intake provides.
- **Let missing sources silently become hallucinated facts** — always mark `source_gap`.
