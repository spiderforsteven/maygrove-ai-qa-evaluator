# Tavily Integration Notes for maygrove-ai-qa-evaluator

The skill uses Tavily (`tvly`) to fill knowledge gaps in Lifestyle, DietCooking, and PlantingTech.

**Important:** Tavily is an optional dependency. The skill must run correctly with only local documents if Tavily is unavailable.

## Prerequisites

```bash
export TAVILY_API_KEY="tvly-..."
# Add to your environment file or pass at runtime.

# Install via pip (preferred; works on any Python runtime)
pip install tavily-cli

# Or use the official installer and verify the signature first:
# curl -fsSL https://cli.tavily.com/install.sh -o /tmp/tavily-install.sh
# review the script, then bash /tmp/tavily-install.sh
```

## Verify

```bash
tvly --version
tvly search "cherry tomato salad recipe" --depth basic --max-results 5 --json
```

## Common Patterns

### Search

```bash
tvly search "cherry tomato salad recipe" --depth basic --max-results 6 --json
```

### Extract a specific page

```bash
tvly extract "https://onepotrecipes.com/cherry-tomato-salad-recipe" --json
```

Output includes `results[0].raw_content`.

## Domain Allowlist (preferred)

- Food/recipes: `seriouseats.com`, `loveandlemons.com`, `onepotrecipes.com`, `recipetineats.com`, `simplyrecipes.com`, `bbcgoodfood.com`
- Gardening/plants: `costafarms.com`, `thespruce.com`, `provenwinners.com`, `extension.org`, `gardeningknowhow.com`
- Lifestyle: `thespruce.com`, `apartmenttherapy.com`, `goodhousekeeping.com`

## Domain Blocklist (avoid)

- E-commerce and price comparison sites
- Forums and unmoderated Q&A
- Social media (Facebook, Pinterest-only pages)
- Video-only pages with no transcript

## Confidence Rules

| Source Type | Confidence Range | Notes |
|---|---|---|
| Extracted full page content | 0.85–0.95 | Use when `raw_content` is clean and complete. |
| Search snippet only | 0.65–0.80 | Mark `source_unverified`. Do not use for precise quantities or safety claims. |
| Multiple sources agree | +0.05 to confidence | Use only if the agreement is on factual details, not generic phrasing. |

## Fallbacks

- If `tvly` is not found: try `pip install tavily-cli`. If still unavailable, disable web research and continue with local sources only.
- If `TAVILY_API_KEY` is missing: disable web research and mark the intent as `web_source_needed`.
- If `tvly extract` fails or returns empty: use the `snippet` from `tvly search` and lower confidence.
- If no reliable source is found after 2 search attempts: route to `rejected/needs_review.jsonl`.
