# Post-Research Figure Generation

Use this reference when the user wants the research cycle to end with static, paper-style figures instead of only Markdown tables or Mermaid blocks.

## Required Inputs

- `paper_pool.csv`: paper metadata, ideally including `paper_id`, `title`, `venue`, `year`, `open_source`, `task`, `modules`, `benchmarks`, and `tags`.
- `idea_matrix.csv`: candidate combinations from `scripts/build_idea_matrix.py`, including `paper_a_id`, `paper_b_id`, `total_score`, and any available scoring dimensions.

The figure script does not invent evidence. It only visualizes fields already present in the research artifacts.

## Command

```bash
python scripts/build_research_figures.py \
  --paper-pool work/paper_pool.csv \
  --idea-matrix work/idea_matrix.csv \
  --output-dir work/figures \
  --topic "Long-Context Reasoning" \
  --prefix long_context \
  --top-k 12
```

## Output Bundle

- `<prefix>_literature_heatmap.png` and `.pdf`: mean candidate scores across paper themes.
- `<prefix>_candidate_scoring_heatmap.png` and `.pdf`: normalized scoring dimensions for the strongest candidates.
- `<prefix>_analysis_panel.png` and `.pdf`: multi-panel analysis of years, venues, score distribution, and top candidates.
- `<prefix>_literature_heatmap_data.csv`: the exact matrix behind the literature heatmap.
- `<prefix>_candidate_scoring_data.csv`: the exact normalized matrix behind the scoring heatmap.
- `<prefix>_figure_manifest.json`: inputs, counts, style contract, and generated files.

## Figure Standards

- Use static PNG for Markdown/GitHub viewing and PDF for manuscript reuse.
- Use colorblind-safe or perceptually uniform palettes.
- Label axes with concrete artifact meaning, not vague words like "quality".
- Use compact titles and avoid decorative effects.
- Keep raw figure data beside the images so readers can audit the visualization.
- Treat all automatically generated scores as screening signals, not final scientific evidence.

## Report Integration

After generating figures, pass the figure directory to the report builder:

```bash
python scripts/build_markdown_report.py \
  --topic "Long-Context Reasoning" \
  --paper-pool work/paper_pool.csv \
  --idea-matrix work/idea_matrix.csv \
  --search-log work/search_log.csv \
  --figure-dir work/figures \
  --figure-prefix long_context \
  --output work/report.md
```

If the figure files are missing, the report builder skips the static figure section instead of inserting broken image links.
