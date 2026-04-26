# Reporting and Visualization

## Goal

Produce a polished Markdown document that is readable, evidence-backed, and visually structured.

## Required Output Qualities

The final report must include:

- a clear executive summary
- visual summaries inside the Markdown document
- detailed analysis, not just recommendations
- explicit analysis basis for each major claim
- a reference list with stable links

## Preferred Visual Forms

Prefer visuals that live directly inside Markdown:

- Mermaid flowcharts for workflow and logic
- Mermaid pie or simple chart blocks for dataset or venue distributions
- Markdown tables for evidence maps
- short callout quotes for key conclusions
- static PNG/PDF figures generated from the research artifacts when the user needs manuscript-style visuals

If the host cannot render Mermaid:

- keep the table-based evidence maps
- replace Mermaid with static images or compact prose blocks

## Post-Research Figure Bundle

When the user asks for literature heatmaps, scoring plots, analysis charts, manuscript figures, or academic paper-style data figures, read `references/figure-generation.md` and run `scripts/build_research_figures.py` after `paper_pool.csv` and `idea_matrix.csv` exist.

The default figure bundle should include:

- literature interaction heatmap: average candidate score across paper themes
- candidate scoring heatmap: normalized scoring dimensions for shortlisted A+B candidates
- analysis panel: paper years, venue distribution, score distribution, and top candidate scores
- backing CSVs and a manifest so the plotted data can be audited

Do not treat these figures as proof of novelty. They are visual summaries of the search and scoring artifacts.

## Recommended Report Structure

1. Title
2. Executive Summary
3. Visual Overview
4. Search Strategy
5. Candidate Landscape
6. Recommended Direction
7. Analysis Basis
8. Detailed Analysis
9. References

## Analysis Basis Rules

Every major claim should trace to one or more of:

- search findings
- paper metadata
- top-candidate matrix scores
- explicit experiment design logic

Good examples:

- "Task overlap is actionable because both papers evaluate on the same benchmark family."
- "Mechanism complementarity is credible because one paper adds memory routing while the other adds verifier control."
- "Implementation tractability is plausible because code exists for both endpoints."

Bad examples:

- "This seems novel."
- "This should work well."
- "The theory is elegant."

Those are conclusions, not bases.

## Citation Rules

- Give every cited paper a stable reference id such as `[R1]`.
- Include title, venue, year, and URL when available.
- Prefer canonical source URLs over random mirrors.
- If the source is a repo or project page rather than a paper, say that explicitly.

## Writing Style

- Prefer short paragraphs and compact tables.
- Do not bury caveats.
- State confidence and boundaries explicitly.
- Keep the document visually calm: a few strong sections, not dozens of shallow bullets.

## Scaffolding

Use `scripts/build_markdown_report.py` to generate the first draft. Then refine:

- tighten the summary
- replace placeholder sentences with actual reasoning
- verify that every major claim still has a basis and a citation

If static figures were generated, pass `--figure-dir <dir>` and `--figure-prefix <prefix>` to embed links to the heatmap, scoring figure, and analysis panel.
