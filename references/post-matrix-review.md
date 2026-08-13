# Post-Matrix Review

## Purpose

Use this procedure after matrix generation to decide which candidate questions deserve researcher attention. Preserve uncertainty and keep every recommendation traceable to source material.

## Review Record

Create one copy of `assets/templates/candidate-review.yaml` per candidate. Keep the matrix artifact unchanged. The review file is the current, revisable interpretation of that candidate.

Use the paper order in `papers` as A then B. Evaluate both directions before setting `selected_direction`:

- `a_to_b`: A may supply a mechanism relevant to B's limitation or open question
- `b_to_a`: B may supply a mechanism relevant to A's limitation or open question
- `bidirectional`: both directions remain meaningfully distinct and supported
- `unknown`: the available evidence does not establish a useful direction

## Data Integrity Stop

Pause review when:

- a paper identifier is missing or resolves to multiple rows
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

## One Review Round

1. Read the matrix row, paper-pool rows, and current review record.
2. Identify the single uncertainty most likely to change the recommendation.
3. Choose one focused action: read a source section, run a targeted search, inspect a repository, or compare benchmark definitions.
4. Add newly verified facts with locators.
5. Add or revise inferences that reference fact identifiers.
6. Update the five qualitative dimensions.
7. Update `status`, `confidence`, `status_reason`, and `next_check`.
8. Append one `review_log` entry.

Starting a review round moves the candidate out of `unreviewed`. If the action cannot obtain enough source evidence for another disposition, use `needs_check`, keep unknown dimensions as `unknown`, and name the missing evidence in `next_check`.

A review-log entry must contain:

```yaml
- round: 1
  question: "The uncertainty examined in this round"
  action: "What was read, searched, inspected, or compared"
  evidence_added: [F1, F2]
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
