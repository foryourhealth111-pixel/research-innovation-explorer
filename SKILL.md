---
name: research-innovation-explorer
description: Explore literature-grounded research innovation ideas and paper framing in a host-neutral way. Use when an AI agent needs to collect a recent paper pool, run broad and deep literature search, decompose methods into reusable capabilities, generate A+B or module-combination candidates, shortlist feasible ideas, design a defensible unifying framework, and produce an elegant Markdown report with citations, analysis rationale, and visual summaries.
---

# Research Innovation Explorer

## Overview

Use this skill to turn a vague "find a publishable idea" request into a disciplined workflow: search broadly, collect strong recent papers, decompose them into reusable capabilities, generate structured candidate combinations, and draft an honest framing plus experiment plan.

Treat this as efficient incremental research planning. Stand on strong prior work, keep claims proportional to evidence, and prefer explicit assumptions over inflated novelty language.

Use this skill as a host-neutral contract. If the current environment supports native Skills, load it with the host's own mechanism. If the environment does not support Skills, follow `SKILL.md`, `references/`, and `scripts/` directly.

## Quick Start

1. Clarify the domain, target venue, resource limits, and whether the user wants concept-only output or a code-ready shortlist.
2. Read `references/host-neutral-usage.md` and adapt invocation to the current host.
3. Read `references/search-playbook.md`, then copy `assets/templates/search-log.csv` to a working file.
4. Run `python scripts/build_search_queries.py --topic "<topic>" --keywords "<comma-separated keywords>"` to generate a search pack.
5. Search across multiple sources, log results, and fill `assets/templates/paper-pool.csv` with 20-50 strong papers.
6. Run `python scripts/build_idea_matrix.py <paper_pool.csv> --output <idea_matrix.csv>` to generate pairwise candidates.
7. Read `references/scoring-rubric.md` to shortlist roughly 10-20 promising combinations.
8. For finalists, read `references/framing-and-theory.md` and write idea briefs with `assets/templates/idea-brief.md`.
9. Read `references/experiment-plan.md` and draft the validation plan with `assets/templates/experiment-plan.md`.
10. Read `references/reporting-and-visualization.md` and run `python scripts/build_markdown_report.py ...` to produce the final Markdown report.

## Workflow

### 1. Use Search Aggressively and Systematically

- Treat search as mandatory during both collection and analysis, not as an optional helper.
- Use the best search surfaces available in the current environment: web search, browse tools, academic search APIs, paper databases, official docs, code search, and repository search.
- Search at multiple depths:
  - broad topic scan
  - targeted method scan
  - benchmark and dataset scan
  - citation chaining
  - negative evidence and failure-case scan
  - code and implementation scan
- Read `references/search-playbook.md` before collecting papers or writing any analysis.

### 2. Build the Paper Pool

- Prefer 20-50 recent, strong, code-accessible papers with real downstream impact.
- Record `task`, `modules`, `strengths`, `weaknesses`, `benchmarks`, and `open_source` for each paper.
- Mix academic papers with strong open-source or industry systems only when they change the practical frontier.
- Read `references/workflow.md` for sourcing rules and intake guidance.

### 3. Decompose Papers into Capabilities

- Rewrite each paper as reusable components, not paper titles.
- Separate task from mechanism: objective, backbone, routing, memory, loss, training recipe, inference trick, evaluator, or data recipe.
- Normalize fields so pairwise comparisons are meaningful.

### 4. Generate Candidate Combinations

- Use `scripts/build_idea_matrix.py` for a first-pass matrix.
- Keep combinations where task overlap is real, mechanisms are complementary, and implementation remains tractable.
- Kill combinations that are purely cosmetic, redundant, or impossible to evaluate with available code and data.
- Read `references/scoring-rubric.md` when the shortlist is noisy or overfull.

### 5. Write the Innovation Hypothesis

- State the claim as a falsifiable hypothesis, not a slogan.
- Prefer forms like:
  - "Method A supplies X that method B lacks under condition C."
  - "A unified controller over A-style and B-style mechanisms should dominate each extreme on regime R."
  - "A shared objective reveals A and B as limiting cases of a broader family."
- Write why the combination should help, what assumption it needs, and where it can fail.

### 6. Frame the Theory Honestly

- Use `references/framing-and-theory.md` before writing any framework section.
- Build a higher-level abstraction only if you can define the latent variable, control knob, objective decomposition, or limiting cases clearly.
- Claim "A and B are special cases" only when the algebra or algorithm really supports it.
- If the work is primarily a strong engineering combination, say so and focus on mechanism plus evidence rather than pretending to have a theorem.
- Read `references/ethics-boundaries.md` whenever claim wording becomes fuzzy.

### 7. Analyze with Search Still Active

- Continue searching during analysis. Do not stop at the first literature dump.
- Search for:
  - adjacent methods that may invalidate the novelty claim
  - older precursor work
  - replication failures
  - benchmark caveats
  - engineering reports or repos that already tried a similar combination
- If the claim changes after new evidence, revise the framing instead of defending the old one.

### 8. Design Proof of Non-Triviality

- Use `references/experiment-plan.md`.
- Always compare against A, B, and the naive composition baseline.
- If using a fusion weight such as `alpha`, sweep the full range rather than cherry-picking one middle value.
- Measure quality, cost, robustness, and failure modes.
- Require at least one ablation that can falsify the claimed mechanism.

### 9. Produce the Final Report

- Use `references/reporting-and-visualization.md`.
- The final Markdown report must include:
  - a readable executive summary
  - visual summaries inside the Markdown document
  - detailed analysis, not only conclusions
  - explicit analysis basis
  - a reference list with stable links
- Use `scripts/build_markdown_report.py` to scaffold the document, then refine it.

## Deliverables

- `search_log.csv`
- `paper_pool.csv`
- `idea_matrix.csv`
- 3-5 shortlisted idea briefs
- one chosen idea with a framing note
- one experiment plan with baselines and ablations
- one polished Markdown report
- optional risk log

## Decision Rules

- If the current host has search or browse tools, use them before relying on memory for current literature claims.
- If the current host has multiple search surfaces, use at least two independent sources for critical literature assertions.
- If no search surface exists, state that limitation explicitly and downgrade confidence.
- Every major claim in the final report must point to a concrete basis: citations, search findings, score evidence, or experiment design logic.
- Prefer Mermaid, Markdown tables, and compact evidence maps for visuals; fall back to static tables when the host cannot render Mermaid.
- Reject any candidate that depends on unavailable code, data, or compute without a fallback plan.
- Reject any "theory" section that cannot name assumptions, variables, and failure boundaries.
- Prefer one sharp, testable incremental contribution over three weakly related tweaks.
- If evidence supports only a narrow regime, say so explicitly.
- Do not fabricate novelty, proofs, citations, experimental wins, or reference metadata.

## Resources

### `scripts/build_search_queries.py`
Use to generate query packs for topic scan, method scan, novelty checks, benchmark checks, and failure analysis.

### `scripts/build_idea_matrix.py`
Use to turn a structured paper pool into scored pairwise candidates.

### `scripts/build_markdown_report.py`
Use to scaffold a polished Markdown report with visual summaries, evidence tables, and references.

### `references/host-neutral-usage.md`
Read to adapt the skill to Codex, Claude Code, Gemini CLI, OpenCode, or a manual workflow.

### `references/search-playbook.md`
Read before literature collection or analysis. This is the search-first operating procedure.

### `references/workflow.md`
Read for the detailed step-by-step process and intake rules.

### `references/scoring-rubric.md`
Read when ranking candidates or pruning the matrix.

### `references/framing-and-theory.md`
Read when writing the "framework", "special case", or "general expression" sections.

### `references/experiment-plan.md`
Read when drafting baselines, ablations, `alpha` sweeps, and evaluation logic.

### `references/reporting-and-visualization.md`
Read when building the final Markdown document and choosing in-document visuals.

### `references/ethics-boundaries.md`
Read when novelty, theory, or claim wording is ambiguous.

### `assets/templates/`
Copy the templates instead of inventing ad hoc tables.
