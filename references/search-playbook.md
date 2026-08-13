# Search Playbook

## Search-First Rule

Do not build the paper pool or write the framing from memory alone when current literature matters. Search first, then reason.

## Search Objectives

Search is used for four distinct jobs:

1. collect candidate papers
2. verify claims and dates
3. find overlapping prior art
4. find negative evidence, caveats, and failed variants

## Minimum Search Pass

When building the paper pool, cover all of these:

1. broad topic scan
2. method-family scan
3. benchmark and dataset scan
4. code and repository scan
5. novelty check
6. negative evidence check

During post-matrix review, do not repeat this full pass for every candidate. Search for the single uncertainty most likely to change the current recommendation, record the result, and choose the next action from the updated evidence.

## Recommended Source Mix

Use at least two source types for important claims.

Primary sources:

- arXiv
- conference or journal pages
- Semantic Scholar
- CrossRef
- PubMed when relevant
- official project pages
- official repositories

Secondary sources:

- general web search
- blog posts from credible labs or companies
- leaderboards

Prefer primary sources whenever they exist.

## Query Strategy

Use `scripts/build_search_queries.py` to generate a starter pack, then adapt queries.

For each topic, search at three granularities:

- topic level
- method level
- evaluation level

Examples:

- topic level: `"long-context reasoning" recent papers`
- method level: `"memory routing" OR "verifier head" long-context reasoning`
- evaluation level: `long-context reasoning benchmark dataset leaderboard`

## Citation Chaining

For every strong seed paper:

- search papers it cites backward
- search papers citing it forward
- search "related papers" or "similar papers"

This step often finds the real nearest neighbors faster than generic search alone.

## Code and Implementation Search

Search for:

- official repos
- reimplementations
- benchmark harnesses
- issues describing failure modes
- ablation tables in repos or docs

If a similar combination already exists in code, downgrade novelty immediately.

## Search During Analysis

Keep searching while writing.

When you draft a claim like:

- "this combination is new"
- "A and B have not been unified"
- "the benchmark regime is underexplored"

run another search pass specifically to challenge that claim.

For a provisional candidate question, preserve missing novelty evidence as `prior_art_risk: uncertain` or `unknown`. Do not turn an incomplete search into a novelty conclusion.

## Search Log Discipline

Log searches in `assets/templates/search-log.csv` with:

- date
- query
- source
- reason for search
- key findings
- follow-up action

This prevents repeated blind searching and makes the evidence trail inspectable.

## Stop Conditions

You can stop searching for a candidate when:

- nearby prior art is mapped well enough
- the evaluation stack is clear
- the claim is bounded and evidence-backed
- additional searches mostly repeat known threads
- the unresolved decision requires researcher input or unavailable access

When stopping before all uncertainty is resolved, record the remaining uncertainty and the next check in the candidate review.
