# Workflow

## Purpose

Use this workflow to search for tractable, literature-grounded incremental research ideas with high implementation leverage.

## Inputs to Collect Up Front

- target domain or topic
- target venue or paper style
- compute and time budget
- available codebases, datasets, or benchmarks
- whether the user wants a concept-only shortlist or a code-ready plan

## Step 0: Prepare the Search Pass

Before collecting papers, read `references/search-playbook.md`.

Then:

- create a `search-log.csv` from `assets/templates/search-log.csv`
- generate a starter query pack with `scripts/build_search_queries.py`
- decide which sources are available in the current host
- prefer at least two independent search surfaces for important claims

## Step 1: Build the Paper Pool

Aim for 20-50 recent, strong papers. A smaller set is fine for a quick pass, but the matrix is only useful when the pool is broad enough.

Selection rules:

- prefer recent papers that were actually noticed by the field
- prefer methods with code or at least reproducible algorithm detail
- include diverse mechanism families, not just many near-duplicates
- keep the task family coherent enough that common evaluation is possible

Search requirements:

- run broad topic search
- run method-family search
- run benchmark and data search
- run novelty check for similar combinations
- run code search for repos and implementations
- log each meaningful search in `search-log.csv`

Record each paper in `paper-pool.csv` with:

- `paper_id`: short stable id such as `A01`
- `title`
- `venue`
- `year`
- `url`
- `open_source`
- `task`
- `modules`
- `strengths`
- `weaknesses`
- `benchmarks`
- `tags`
- `notes`

## Step 2: Decompose Papers into Capabilities

Convert each paper into reusable parts:

- task formulation
- model family
- routing or control logic
- memory or retrieval subsystem
- training objective
- inference trick
- data or augmentation recipe
- evaluation advantage

Write these as semicolon-separated fragments so the script can compare them.

## Step 3: Generate the Candidate Matrix

Run:

```bash
python scripts/build_idea_matrix.py paper-pool.csv --output idea-matrix.csv
```

This creates a scored pairwise table. Treat it as a triage tool, not as the final judge.

If the matrix looks promising too quickly, run another novelty check before trusting it.

## Step 4: Rapid Technical Triage

Discard candidates with any of these problems:

- no meaningful shared task or benchmark space
- same mechanism family with no new control variable
- unavailable code, data, or compute with no practical fallback
- no clear hypothesis beyond "maybe two good things are better together"

Keep candidates where:

- mechanism complementarity is real
- one method's strength plausibly addresses the other's weak regime
- implementation path is clear
- evaluation can be done with existing baselines

## Step 5: Write Idea Briefs

For the strongest 3-5 candidates, use `assets/templates/idea-brief.md`.

Each brief should capture:

- the combined hypothesis
- why the pairing is complementary
- the exact control variable or composition pattern
- what makes the work more than a cosmetic ensemble
- what failure mode would kill the idea

## Step 6: Build the Framing

Use `references/framing-and-theory.md`.

Good framing patterns:

- one objective family with two limiting cases
- one controller or gate over two mechanism families
- one constraint relaxation that recovers earlier methods
- one two-stage decomposition where each paper occupies a clear role

Bad framing patterns:

- renaming a weighted sum and calling it a theory
- claiming universality without assumptions
- hiding that the contribution is mainly engineering integration

While framing, keep search active. Search again whenever a claim depends on novelty, precedence, or benchmark coverage.

## Step 7: Design the Validation Plan

Use `references/experiment-plan.md` and `assets/templates/experiment-plan.md`.

The plan should prove one of these:

- better peak quality than both endpoints
- better quality-cost tradeoff
- better robustness in the regime the framing predicts

## Expected Outputs

- one populated `paper-pool.csv`
- one scored `idea-matrix.csv`
- 3-5 idea briefs
- one chosen framing note
- one experiment plan
