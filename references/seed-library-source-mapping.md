# MayGrove AI QA: Seed Library Source Mapping

This document maps the 50-variety MayGrove seed library to the 7 intent categories used in the Q&A evaluation set.

## Seed Library Overview

**File:** `种菜机种子挑选50种2026.6.12_Steven_2_.xlsx`

**Coverage:**
- 4 major categories (37 valid entries after cleaning)
- 50 varieties total (with some duplicate names in different subcategories)
- Key fields per variety: category, plant name, variety name, app name, plant ID, is_climbing, is_organic, germination days, seedling days, vegetative days, flower/fruit days, harvest/maturity days, temperature range (℉), harvest type, description, URL, SKU, seed availability status, needle color, first-batch selection flag

**Categories:**

| Category | Count | Typical plants |
|---|---|---|
| Herbs | 9 | Catnip, Rosemary, Peppermint, Parsley, Lemon Balm, Chives, Basil (3 varieties) |
| Greens | 20 | Lettuce, Kale, Swiss Chard, Pak Choi, Mustard, Arugula, Endive, Collards, Celery, Cabbage, Amaranth |
| Fruit Vegetables | 7 | Radish, Pepper (5 varieties), Eggplant |
| Climbing | 7 | Tomato (4 varieties), Pea, Cucumber (2 varieties), Bean |
| Flowers | 3 | Zinnia, Sunflower, Calendula |

*(Note: After cleaning empty rows, 37 valid entries remain in the main sheet.)*

---

## First-Batch Selected Varieties (10 plants)

These are the varieties explicitly marked for the first shipment. They are critical for answering "what should I grow first?" and "what's included in the seed kit?" questions.

| # | Plant | Variety | Category | Notes |
|---|---|---|---|---|
| 1 | Lettuce | Romaine - Cimmaron | Greens | 60–70 days, deep-red head, crisp |
| 2 | Lettuce | Gourmet Mixture | Greens | 35–70 days, mixed lettuce types |
| 3 | Lettuce | Butterhead - All Year Round | Greens | 35–45 days, tender butterhead |
| 4 | Kale | Classic Kale (Vates Blue Scotch Curled) | Greens | 35–50 days, cold-hardy, curly |
| 5 | Endive | Frisee | Greens | 35–50 days, frilly yellow-green leaves |
| 6 | Arugula | Slow Bolt (Organic) | Greens | 25–35 days, fast-growing |
| 7 | Radish | Cherry Belle (Organic) | Fruit Vegetables | 25–30 days, very fast |
| 8 | Zinnia | Thumbelina Mixture | Flowers | 50–59 days, dwarf ornamental |
| 9 | Cucumber | Beit Alpha F1 CMR/MMR | Climbing | 51–90 days, burpless, parthenocarpic |
| 10 | Tomato | Large Red Cherry | Climbing | 75–120 days, indeterminate cherry |

---

## Climbing Varieties (Must Use Bottom Pods + Trellis)

These must be planted in the bottom 3 pods and require the trellis system.

| Plant | Variety | App Name | Notes |
|---|---|---|---|
| Tomato | Cherry Tomato - Currant Yellow | Tomato Seeds - Cherry - Currant Yellow | Indeterminate, 75–120 days |
| Tomato | Tomato- Salad | Tomato Seeds - Salad - Celebrity Plus Hybrid | Semi-determinate, 75–90 days, AAS winner |
| Pea | Snow - Oregon Giant (Organic) | Pea Seeds - Snow - Oregon Giant (Organic) | 65–75 days, powdery mildew resistant |
| Cucumber | Beit Alpha F1 CMR/MMR | Cucumber Seeds - Beit Alpha F1 CMR/MMR | 51–90 days, burpless, parthenocarpic |
| Cucumber | Sweet Success Hybrid | Cucumber Seeds - Sweet Success Hybrid | 53–90 days, seedless, 14 inch fruits |
| Bean | Pole - Blue Lake FM1K | Bean Seeds - Pole - Blue Lake FM1K | 61–90 days, pole snap bean |
| Tomato | Cherry Tomato-Red | Large Red Cherry Tomato | 75–120 days, indeterminate |

---

## Intent-to-Seed Mapping

### PlantingTech

**Directly supported by seed library:**
- Variety-specific germination time, seedling time, vegetative time, harvest time
- Temperature range per variety
- Climbing vs non-climbing placement rules
- Harvest type: continuous vs single
- Organic vs non-organic variety flag

**Example QA topics:**
- "How long does Romaine Cimmaron take from seed to harvest?" → 60–70 days
- "Can I grow Large Red Cherry Tomato in any pod?" → No, must be bottom pod + trellis
- "What temperature range is best for Arugula?" → 50–68 ℉
- "Is Cherry Belle radish a continuous harvest or single harvest?" → single
- "Which herbs are included in the seed options?" → Catnip, Rosemary, Peppermint, Parsley, Lemon Balm, Chives, Basil

### ProductInquiry

**Directly supported by seed library:**
- First-batch included varieties
- Climbing plant compatibility with V30 bottom pods
- Whether a plant is organic
- Seed availability / verification status
- Whether third-party seeds can be used (manual §15.5 says yes, but seed library confirms what MayGrove offers)

**Example QA topics:**
- "What seeds come in the first shipment?" → 10 varieties listed above
- "Do I have to use MayGrove seeds?" → No, but MayGrove seed library offers these 50 varieties
- "Which plants need the trellis?" → Tomato, Pea, Cucumber, Bean
- "Is the Arugula seed organic?" → Yes, Slow Bolt is marked organic

### GrowingPlan

**Directly supported by seed library:**
- Beginner-friendly first-batch varieties
- Fast-harvest options (Arugula 25–35 days, Radish 25–30 days)
- Longer-cycle options (Tomato 75–120 days, Cucumber 51–90 days)
- Variety combinations for the 30 + 2 capacity
- Seedling nursery usage: 12 slots can start some varieties before transplanting

**Example QA topics:**
- "I'm a beginner. What should I plant first?" → First-batch 10 varieties, especially lettuce/arugula/radish
- "Can I plan a mix of fast and slow crops?" → Yes, combine radish (25–30d) with tomato (75–120d)
- "How many plants can I grow at once?" → 30 main pods + 12 seedling pods
- "Which plants should go in the seedling box?" → Most can start there; fast greens like lettuce/arugula are common choices

### Lifestyle

**Directly supported by seed library:**
- Kitchen-friendly herbs (Basil, Parsley, Chives, Mint, Rosemary)
- Gift-friendly plants (Zinnia, Sunflower, Calendula, low-maintenance lettuce)
- Kid-friendly fast-growing plants (Radish, Arugula, Sunflower, Zinnia)
- Home décor: flowering plants for color

**Example QA topics:**
- "What can I grow in the kitchen that I can use while cooking?" → Basil, Parsley, Chives, Rosemary, Peppermint
- "What flowering plants can I grow for decoration?" → Zinnia, Sunflower, Calendula
- "What fast-growing plants can kids help with?" → Radish, Arugula, Sunflower, Zinnia, Lettuce
- "What plants make good gifts?" → Flowering plants, herb mixes, or easy lettuce varieties

### DietCooking

**Directly supported by seed library + nutrition sheet:**
- Nutrition facts per variety (vitamins, minerals, calories, protein, fiber)
- Edible plant parts (leaves for lettuce, fruits for tomato/pepper, pods for pea/bean, roots for radish)
- Food safety: wash before eating, pet toxicity for some plants
- Recipe pairings: Basil→pesto, Tomato→salad, Pepper→stir-fry, Cucumber→salad, Radish→salad

**Example QA topics:**
- "How much Vitamin K is in basil?" → 414.8 µg
- "What can I make with my basil harvest?" → Pesto, caprese, tomato-basil salad
- "Are the plants safe for my cat?" → Some may be toxic; consult a vet (V30 manual §15.12)
- "What's a simple recipe for cherry tomatoes?" → Cherry tomato salad with herbs, lemon, olive oil
- "Which plant is high in Vitamin C?" → Parsley (133 mg), Peppermint (31.8 mg), Kale (93.4 mg)

### ChatEmotional

**Not directly supported by seed library** (personality/tone domain). Use Maygrove.md persona rules instead. However, seed library can be used for lighthearted "excited about harvest" questions.

**Example QA topics:**
- "My first lettuce is almost ready! What should I expect?" → Encouraging tone + harvest guidance
- "I'm so proud of my basil. Any recipe ideas to celebrate?" → Persona-aligned encouragement + recipe suggestion

### OutofScope

**Not supported by seed library.** Use brand boundary policy.

**Example QA topics:**
- "What stocks should I buy?" → Deflect to planting topics
- "Can you diagnose my medical symptoms?" → Deflect to professional help
- "Write Python code for me." → Deflect to MayGrove-related topics

---

## Confidence Rules for Seed-Library Facts

| Fact Type | Confidence | Notes |
|---|---|---|
| Days to harvest from seed library | 0.95–1.0 | Directly from the table |
| Temperature range from seed library | 0.95–1.0 | Directly from the table |
| Climbing requirement | 0.95–1.0 | Combined with V30 manual §12.1 |
| First-batch selection | 0.95–1.0 | Directly from the table (✓ flag) |
| Nutrition data | 0.90–0.95 | From the 种子营养成份整理模版 sheet |
| Recipe suggestions | 0.75–0.85 | Usually from web research; seed library tells what is available |
| Pet toxicity of a specific plant | 0.70–0.80 | General warning from V30 manual; specific toxicity per variety requires web research |

---

## Handling Seed Library Gaps

| Gap | Handling |
|---|---|
| Some rows have missing seed status or unverified varieties | Do not claim availability for specific varieties unless the table says "有种子，已验证" |
| Plant-specific pest/disease advice | Use V30 manual general guidance + web research; mark confidence accordingly |
| Exact flavor/yield claims | Keep close to seed description; avoid exaggeration |
| Planting difficulty (Easy / Medium / Advanced) | Mentioned in the 630补充信息 sheet but not fully populated; use the 种植Tips整理模版 category-level difficulty |

---

## Usage in the Pipeline

1. **Source Loader** converts the Excel into structured seed records (one per variety) and the 种植Tips整理模版 into category-level care guides.
2. **FactAgent A** extracts literal values from the table.
3. **FactAgent B** synthesizes cross-category rules (e.g., "climbing plants must use bottom pods + trellis").
4. **FactAgent C** (web) only fills gaps like specific pet toxicity or recipe ideas.
5. **QAAgents** use the seed records to generate plant-specific questions.
6. **Critics** verify that every variety-specific claim is traceable back to the seed library or a cited web source.
