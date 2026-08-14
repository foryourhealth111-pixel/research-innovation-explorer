# Reporting and Visualization

## Default Goal

Produce a researcher-facing candidate landscape that makes review priorities, evidence, uncertainty, and next checks easy to inspect. Treat it as a provisional screening artifact.

## Required Sections

Include:

1. an executive summary of the reviewed landscape
2. review coverage and important coverage limits
3. promising candidates
4. candidates marked `needs_check` or `conflicting`
5. candidates marked `parked`, `weak`, or `excluded`
6. detailed evidence records for highlighted candidates
7. stable source links

For each highlighted candidate, show:

- matrix rank and score as triage signals
- qualitative status and confidence
- both direction assessments and their supporting inference identifiers
- selected direction and possible research question or questions
- observed facts with source locators
- agent inferences linked to fact identifiers
- closest concern and key uncertainty
- next recommended check

## Separation Rules

- Display matrix score and qualitative judgment in different columns or fields.
- Describe matrix-derived values as screening signals.
- Do not use matrix score to establish mechanism complementarity, novelty, feasibility, publishability, or expected success.
- Distinguish source facts from agent interpretation visually.
- Preserve support and contrary evidence when sources conflict.
- Give parked, weak, and excluded candidates a concrete status reason.

## Preferred Visual Forms

Use visuals only when they help compare the landscape:

- Mermaid flowcharts for the review process
- Markdown tables for candidate and evidence comparison
- static heatmaps or analysis panels for matrix-level screening patterns
- compact callouts for consequential uncertainty

Label generated matrix figures as screening views. Keep the backing CSV files beside static figures.

## Recommended Structure

1. Title
2. Executive Summary
3. Review Coverage
4. Priority Candidates
5. Needs Check and Conflicting Evidence
6. Parked, Weak, and Excluded Candidates
7. Detailed Candidate Evidence
8. References

Use `assets/templates/analysis-report-template.md` as the default structure.

## Citation Rules

- Give every cited paper or repository a stable reference identifier.
- Include title, venue or source type, year, and canonical URL when available.
- Locate important evidence by section, page, figure, table, appendix, file path, symbol, issue, or commit.
- State when a source is secondary or when only an abstract was available.

## Matrix Overview Scaffold

`scripts/build_markdown_report.py` reads `paper-pool.csv`, `idea-matrix.csv`, and `search-log.csv`. Use it to produce a matrix overview, candidate ranking table, figure links, and reference scaffold.

The script does not read `candidate-review.yaml`. After generation, replace its placeholders and matrix-only interpretations with reviewed facts, inferences, statuses, uncertainty, and next checks from the candidate review records.

When the user requests publication-style reporting for a selected candidate, expand the document only after the corresponding research review or validation work exists.
