# Session Evidence: MayGrove QA Evaluation Skill Build

Date: 2026-07-16
Session goal: Validate that the 7-intent Q&A evaluation pipeline works with local documents and Tavily web research.

## Documents used

- `/home/hermeswebui/.hermes/webui/attachments/af101c1faf05/MayGrove_Verti_30__V30__使用说明书.md` (V30 hardware manual)
- `/home/hermeswebui/.hermes/webui/attachments/af101c1faf05/Maygrove.md` (App requirements/test cases)

## Pipeline validated

1. Source Loader split the manual into 83 fact chunks.
2. Fact Extractor selected representative chunks for each intent.
3. User Simulator + QA Generator produced 11 Q&A pairs.
4. Critic / Verifier marked all 11 as verified (with lower confidence for web-research items).
5. WebResearch Agent used Tavily to fetch recipe and lifestyle facts and close source gaps.

## Generated outputs (workspace demo)

- `/workspace/.hermes/plans/maygrove-demo/verified_intent_qa.jsonl`
- `/workspace/.hermes/plans/maygrove-demo/verified_intent_qa.csv`
- `/workspace/.hermes/plans/maygrove-demo/web_research/diet_research.json`
- `/workspace/.hermes/plans/maygrove-demo/web_research/lifestyle_research.json`
- `/workspace/.hermes/plans/maygrove-demo/web_research/web_facts.json`

## Key findings

- PlantingTech, ProductInquiry, and OutofScope are well-covered by the manual.
- GrowingPlan and ChatEmotional are well-covered by `Maygrove.md`.
- Lifestyle and DietCooking require web research for concrete recommendations.
- Tavily CLI (`tvly 0.1.4`) is available at `~/.hermes/home/.local/bin/tvly` and works for `search` + `extract`.
- Web-research facts must be human-summarized into atomic facts before generating Q&A.

## Web sources used in this session

- `onepotrecipes.com/cherry-tomato-salad-recipe`
- `loveandlemons.com/pesto-recipe`
- `bubblysideoflife.com/cocktails-with-fresh-mint`
- `costafarms.com/blogs/get-growing/perfect-plants-for-kitchens`
- `livelyroot.com/collections/plants-as-gifts`
- `seacoast.macaronikid.com/articles/6423498cde90a9104fd91ffb/easy-care-indoor-plants-for-kids-to-grow`
