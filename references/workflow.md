# Workflow

## Purpose

Use this workflow to build a literature-grounded candidate landscape that helps a researcher choose which questions deserve further investigation.

## Inputs to Collect Up Front

- target domain or topic
- resource and time constraints
- available codebases, datasets, and benchmarks
- preferred breadth of the review queue
- researcher-requested papers or combinations
- desired output language

## Step 0: Prepare the Search Pass

Read `references/search-playbook.md`, then:

- create a working `search-log.csv` from `assets/templates/search-log.csv`
- generate a starter query pack with `scripts/build_search_queries.py`
- identify the search surfaces available in the current host
- prefer at least two source types for important literature facts

## Step 1: Build the Paper Pool

Aim for 20-50 papers. A smaller set can support a quick exploration, provided the final output states the coverage limitation.

Selection guidance:

- include recent papers and relevant precursors
- prefer methods with source code or reproducible algorithm detail
- include varied mechanism families
- keep enough task coherence for meaningful comparison
- include negative results or boundary studies when they change interpretation
- assign one non-empty, unique `paper_id` to every retained paper

Record each paper in `paper-pool.csv` with:

- `paper_id`: stable identifier such as `A01`
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
- inference method
- data or augmentation recipe
- evaluation advantage

Write comparable concepts as semicolon-separated fragments. Preserve uncertainty in `notes`; do not fill a field with an inferred capability as though the paper stated it.

## Step 3: Generate the Candidate Matrix

Run:

```bash
python scripts/build_idea_matrix.py paper-pool.csv --output idea-matrix.csv
```

The matrix rejects duplicate paper identifiers, sorts papers by `paper_id`, and then enumerates and ranks unique pairs using lightweight textual and metadata signals. Use `total_score` to order review effort. Keep it separate from later qualitative judgment.

## Step 4: Build the Review Queue

Construct one queue in this order:

1. Take the ten highest-ranked unique paper pairs.
2. Add up to five remaining pairs that increase coverage across tasks or mechanism families.
3. Add every researcher-requested pair, regardless of matrix rank.

Treat `(A, B)` and `(B, A)` as the same pair when removing duplicates. Preserve the matrix row's canonical `paper_a_id` and `paper_b_id`, set `candidate_id` to `<paper_a_id>__<paper_b_id>`, and inspect both directions during review.

If fewer candidates exist, review the available set. If the researcher requests a different queue size, use that size and record the override.

## Step 5: Check Reviewability

Before interpreting a candidate, confirm:

- both paper identifiers resolve to exactly one paper-pool row
- the identifiers are non-empty, distinct, and remain in canonical matrix order
- the rows are not template or placeholder data
- titles and source URLs identify real papers
- the matrix row is readable

Stop that candidate on broken data, record the issue outside the research-status field, and resume after repair.

## Step 6: Run the Dynamic Review

Read `references/post-matrix-review.md` and copy `assets/templates/candidate-review.yaml` for each candidate.

For every candidate:

1. Verify the relevant task, mechanism, result, and limitation statements against source material.
2. Assess A-to-B under `direction_checks.a_to_b` and link the assessment to inference identifiers.
3. Assess B-to-A under `direction_checks.b_to_a` and link the assessment to inference identifiers.
4. Select `a_to_b`, `b_to_a`, `bidirectional`, or `unknown` only after both checks are populated.
5. Link a non-unknown selection through `selection_inference_ids`.
6. Identify the single uncertainty most likely to change the current recommendation.
7. Perform one focused search, reading, repository inspection, or benchmark comparison.
8. Add observed facts and source-linked inferences.
9. Update qualitative dimensions, status, confidence, status reason, `status_inference_ids`, and next check.
10. Run `scripts/validate_candidate_review.py` on the populated record.
11. Repeat only while a new action is likely to change the recommendation.

## Step 7: Produce the Candidate Landscape

Use `references/reporting-and-visualization.md` and `assets/templates/analysis-report-template.md`.

Group candidates as:

- promising
- needs check or conflicting
- parked, weak, or excluded

For each highlighted candidate, show both direction assessments, the selected direction, possible question or questions, observed facts, agent inferences, closest concern, unresolved uncertainty, and next check. Display the matrix score as a separate triage signal.

## Optional Expansion

Proceed only when the researcher asks to deepen a selected candidate:

- framing note: use `references/framing-and-theory.md`
- validation plan: use `references/experiment-plan.md`
- screening figures: use `references/figure-generation.md`
- extended Markdown report: use the report script as a scaffold and merge in reviewed evidence

## Expected Default Outputs

- one populated `search-log.csv`
- one populated `paper-pool.csv`
- one scored `idea-matrix.csv`
- review records for the candidates actually examined
- one provisional candidate landscape with evidence, uncertainty, and next checks
