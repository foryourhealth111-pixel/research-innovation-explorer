# Post-Matrix Review

## Purpose

Use this procedure after matrix generation to decide which candidate questions deserve researcher attention. Preserve uncertainty and keep every recommendation traceable to source material.

## Review Record

Create one copy of `assets/templates/candidate-review.yaml` per candidate. Keep the matrix artifact unchanged. The review file is the current, revisable interpretation of that candidate.

Copy `paper_a_id` and `paper_b_id` from the matrix row. The matrix generator sorts papers by identifier, so these roles remain stable. Set `candidate_id` to `<paper_a_id>__<paper_b_id>`.

Record both directions under `direction_checks`. Use these assessment values:

- `unreviewed`: this direction has not entered a focused review
- `unknown`: a focused review was completed but did not establish the relationship
- `supported`: source-linked inferences support a bounded question in this direction
- `not_supported`: a focused review found no meaningful question in this direction
- `conflicting`: credible evidence supports incompatible interpretations of this direction

Each `supported`, `not_supported`, or `conflicting` assessment must reference at least one inference identifier. An `unknown` assessment must name its key uncertainty. Evaluate both directions before setting `selected_direction`:

- `a_to_b`: A may supply a mechanism relevant to B's limitation or open question
- `b_to_a`: B may supply a mechanism relevant to A's limitation or open question
- `bidirectional`: both directions remain meaningfully distinct and supported
- `unknown`: the available evidence does not establish a useful direction

Do not make a non-unknown selection while either direction remains `unreviewed`. Use `bidirectional` only when both direction assessments are `supported` and both contain inference identifiers. A one-way selection must cite an inference from the selected direction; a bidirectional selection must cite at least one inference from each direction.

Before including a populated record in the candidate landscape, run:

```bash
python scripts/validate_candidate_review.py work/<candidate-id>.yaml
```

## Data Integrity Stop

Pause review when:

- a paper identifier is missing or resolves to multiple rows
- the paper identifiers are equal or do not match the matrix row's canonical A/B order
- `candidate_id` does not equal `<paper_a_id>__<paper_b_id>`
- the candidate points to an absent paper
- the row contains template or placeholder data
- the source cannot identify the claimed paper
- the matrix or paper-pool record is malformed

Record the problem in `data_issue` and leave `status: unreviewed`. Repair the input, clear `data_issue`, then restart the candidate from `unreviewed`.

## Evidence Records

Every observed fact must contain:

```yaml
- fact_id: F1
  statement: "A claim directly supported by the source"
  source_url: "https://stable-source.example/item"
  locator: "Section 4.2, Table 3, page 8"
```

Use a paper, official supplement, official project page, or official repository whenever available. A locator may be a section, page, figure, table, appendix, file path, symbol, issue, or commit.

Every agent inference must contain:

```yaml
- inference_id: I1
  statement: "A cautious interpretation of the candidate relationship"
  fact_ids: [F1, F2]
```

Do not place interpretations in `observed_facts`. Do not claim absence from a failed or incomplete search. Record it as an unresolved question and describe the search coverage.

Fact and inference identifiers must be non-empty and unique within the record. Every referenced identifier must resolve to exactly one record entry. Use direction-check `inference_ids` for directional judgments, `selection_inference_ids` for a non-unknown selected direction, and `status_inference_ids` for a decisive research status. A `needs_check` status may instead name the missing evidence in `status_reason` and provide a concrete `next_check`.

## One Review Round

1. Read the matrix row, paper-pool rows, and current review record.
2. Identify the single uncertainty most likely to change the recommendation.
3. Choose one focused action: read a source section, run a targeted search, inspect a repository, or compare benchmark definitions.
4. Add newly verified facts with locators.
5. Add or revise inferences that reference fact identifiers.
6. Update the relevant direction check and its `inference_ids`.
7. After both directions have been checked, update `selected_direction` and `selection_inference_ids`.
8. Update the five qualitative dimensions for the selected direction or pair.
9. Update `status`, `confidence`, `status_reason`, `status_inference_ids`, and `next_check`.
10. Append one `review_log` entry.

Starting a review round moves the candidate out of `unreviewed`. If the action cannot obtain enough source evidence for another disposition, use `needs_check`, keep unknown dimensions as `unknown`, and name the missing evidence in `next_check`.

A review-log entry must contain:

```yaml
- round: 1
  direction_checked: a_to_b
  question: "The uncertainty examined in this round"
  action: "What was read, searched, inspected, or compared"
  evidence_added: [F1, F2]
  inferences_added: [I1]
  previous_status: unreviewed
  new_status: needs_check
  judgment_change: "What changed and why"
```

## Research Question Shape

Prefer a bounded question:

> Under setting S, can mechanism M from A address limitation L observed in B, as measured by evaluation E?

Use the source record to fill S, M, L, and E. Leave an element unresolved when the evidence does not support it.

## Status and Confidence

Assign statuses using `references/scoring-rubric.md`. Status expresses the current disposition of the candidate. Confidence expresses how well the current disposition is supported.

Apply the five qualitative dimensions and the overall research status to the selected direction. For `bidirectional`, apply them to the pair-level recommendation while retaining both direction-specific questions and uncertainties.

Confidence anchors:

- `low`: key facts are missing, indirect, or weakly located
- `medium`: the main interpretation has direct support, with an important unresolved issue
- `high`: multiple directly located facts support the current disposition and targeted checks found no material contradiction

Confidence is not a probability of research success.

## Stop Conditions

Stop the current candidate when any of these applies:

- additional searches mainly repeat mapped sources or findings
- the record supports a clear current status and a concrete next check
- the decisive uncertainty requires researcher judgment, unavailable access, or work outside the requested scope
- a data-integrity problem prevents reliable interpretation

When stopping with uncertainty, use `needs_check`, `conflicting`, or `unknown` fields as appropriate. Preserve the next action that would reduce the uncertainty.

## Reopening

All research statuses are revisable. Reopen a candidate when new literature, a corrected source, researcher feedback, or changed resource constraints could alter the status. Append a new review round and retain earlier entries.
