<div align="center">

# Research Innovation Explorer

**A host-neutral, search-first skill for literature-grounded idea discovery, theory framing, and polished Markdown reporting.**

[中文文档](./README.zh-CN.md)

[![GitHub stars](https://img.shields.io/github/stars/foryourhealth111-pixel/research-innovation-explorer?style=flat-square)](https://github.com/foryourhealth111-pixel/research-innovation-explorer)
[![GitHub repo size](https://img.shields.io/github/repo-size/foryourhealth111-pixel/research-innovation-explorer?style=flat-square)](https://github.com/foryourhealth111-pixel/research-innovation-explorer)
![Host-neutral](https://img.shields.io/badge/host-neutral-111827?style=flat-square)
![Search-first](https://img.shields.io/badge/search-first-0f766e?style=flat-square)
![Markdown reporting](https://img.shields.io/badge/reporting-markdown%20%2B%20visuals-7c3aed?style=flat-square)

</div>

## Why This Exists

Most research-idea workflows fail in one of three ways:

- they rely on vague intuition instead of systematic search
- they generate combinations but cannot explain why the combination matters
- they stop at analysis and never produce a clean, evidence-backed report

`research-innovation-explorer` is built to close those gaps with one coherent workflow:

1. Search broadly and repeatedly.
2. Decompose papers into reusable capabilities.
3. Generate and score candidate combinations.
4. Frame the strongest hypothesis honestly.
5. Finish with a polished Markdown report that includes citations, analysis basis, and visual summaries.

## Core Methodology

This skill is built around one explicit research-production loop:

1. Collect roughly 40 recent, top-tier, oral-level, open-source, industry-recognized papers.
2. Build a `40 x 40` directional combination matrix over those papers.
3. Remove the diagonal self-pairs and keep the remaining `40 x 39 = 1560` possible `A + B` combinations.
4. Run fast logical checks, lightweight experiments, and targeted search passes on those 1560 candidates.
5. Use the evidence to filter the space down to roughly 15 ideas that are actually defensible and runnable.

This is the operational core of the workflow, not a side note. The point is not to wait for a single flash of inspiration. The point is to search comprehensively, force structured combination, validate aggressively, and only then keep the few ideas that survive contact with evidence.

| Stage | What to do | What comes out |
| --- | --- | --- |
| Paper pool | Gather around 40 strong recent papers with code and real impact | a reusable capability inventory |
| Combination pass | Enumerate the `40 x 40` space and remove self-pairs | 1560 directional `A + B` candidates |
| Fast validation | Search prior work, inspect code, run quick logic checks or minimal experiments | a smaller set of realistic options |
| Final shortlist | Keep only combinations that remain novel enough, coherent enough, and implementable enough | about 15 viable ideas |

## What You Get

| Layer | What it does |
| --- | --- |
| `SKILL.md` | Defines the end-to-end workflow and decision rules |
| `scripts/build_search_queries.py` | Generates structured query packs for topic scan, novelty checks, and failure analysis |
| `scripts/build_idea_matrix.py` | Builds a scored pairwise candidate matrix from the paper pool |
| `scripts/build_markdown_report.py` | Scaffolds a polished Markdown report with Mermaid visuals, evidence tables, and references |
| `references/` | Contains the search playbook, theory framing rules, reporting rules, and ethics boundaries |
| `assets/templates/` | Provides ready-to-use CSV and Markdown templates for search logs, paper pools, idea briefs, experiment plans, and reports |

## Workflow

```mermaid
flowchart LR
    A[Search Pass] --> B[Paper Pool]
    B --> C[Capability Decomposition]
    C --> D[Idea Matrix]
    D --> E[Shortlist]
    E --> F[Theory Framing]
    F --> G[Experiment Plan]
    G --> H[Markdown Report]
```

## Design Principles

### 1. Search First

The skill assumes that current literature claims should not come from memory alone when search is available.

### 2. Honest Framing

It supports strong abstraction and theory writing, but only when the assumptions, limiting cases, and failure boundaries are real.

### 3. Evidence-Carrying Reports

The final Markdown output is not a pretty wrapper around intuition. It must include:

- citations
- explicit analysis basis
- candidate comparison
- visual summaries

### 4. Host Neutrality

The workflow is portable across different agent hosts and even manual use. The repo does not depend on one specific runtime.

## Quick Start

### 1. Prepare the search pack

```bash
python scripts/build_search_queries.py \
  --topic "long-context reasoning" \
  --keywords "memory routing, verifier head, benchmark"
```

### 2. Build the paper pool

Start from:

- `assets/templates/search-log.csv`
- `assets/templates/paper-pool.csv`

### 3. Generate the idea matrix

```bash
python scripts/build_idea_matrix.py \
  assets/templates/paper-pool.csv \
  --output work/idea-matrix.csv
```

### 4. Generate the Markdown report

```bash
python scripts/build_markdown_report.py \
  --topic "Long-Context Reasoning" \
  --paper-pool assets/templates/paper-pool.csv \
  --idea-matrix work/idea-matrix.csv \
  --search-log assets/templates/search-log.csv \
  --output work/report.md
```

## Output Style

The reporting layer is intentionally designed for GitHub-native reading:

- Mermaid flowcharts for process explanation
- Mermaid pie charts for quick distribution views
- Markdown evidence tables for claim tracing
- compact narrative sections for executive summary and detailed analysis

This makes the output readable both as a working note and as a shareable artifact.

## Repository Layout

```text
.
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── templates/
├── references/
└── scripts/
```

## Recommended Use Cases

- discovering incremental but defensible research ideas
- mapping literature around a topic before starting implementation
- checking whether an A+B combination already exists in prior work or code
- producing a strong Markdown research memo with citations and visual summaries
- training literature review, abstraction, evaluation design, and research writing habits

## Documentation

- Core workflow: [`SKILL.md`](./SKILL.md)
- Search protocol: [`references/search-playbook.md`](./references/search-playbook.md)
- Theory framing: [`references/framing-and-theory.md`](./references/framing-and-theory.md)
- Reporting rules: [`references/reporting-and-visualization.md`](./references/reporting-and-visualization.md)
- Report template: [`assets/templates/analysis-report-template.md`](./assets/templates/analysis-report-template.md)

## Notes

- If your host cannot render Mermaid, keep the Markdown tables and replace Mermaid blocks with static images or plain-text summaries.
- If your host has no search capability, use the workflow manually and explicitly downgrade confidence in current-literature claims.

## Community

For broader discussion around tools, workflows, and AI-native building, visit [linux.do](https://linux.do/).
