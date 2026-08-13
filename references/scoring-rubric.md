# Qualitative Review Rubric

## Purpose

Use this rubric after matrix generation to describe a candidate consistently. Do not convert these judgments into a total score. Keep the matrix score as a separate queue-priority signal.

## Qualitative Dimensions

### Task Relation

- `close`: both papers address the same task or a directly shared operating regime
- `adjacent`: the tasks differ, with a source-supported shared subproblem or transfer setting
- `loose`: the connection depends mainly on broad topic similarity
- `unknown`: the available sources do not establish the relationship

### Mechanism Relation

- `complementary`: located evidence supports a distinct role for each mechanism in the proposed question
- `partly_complementary`: one useful connection is supported, while scope or direction remains uncertain
- `unclear`: textual difference exists without enough evidence for functional complementarity
- `unknown`: relevant mechanism detail has not been verified

### Question Clarity

- `clear`: setting, mechanism, limitation, and observable outcome can be stated concretely
- `vague`: at least one essential element remains too broad for a focused follow-up
- `unknown`: source coverage is insufficient to form the question

### Prior-Art Risk

- `low`: a targeted search mapped nearby work and found a distinguishable question within the searched scope
- `uncertain`: search coverage is incomplete or nearby work may overlap
- `high`: a source describes the same combination or substantially the same research question
- `unknown`: no targeted prior-art check has been completed

### Implementation Friction

- `low`: compatible code, data, evaluation, and resource requirements are documented
- `medium`: one material integration or resource issue remains
- `high`: several material dependencies are missing or exceed declared constraints
- `unknown`: implementation requirements have not been checked

## Status Assignment

- `unreviewed`: no review round has started; only matrix information is available
- `promising`: the question is clear, at least one source-linked mechanism relation supports it, and remaining concerns can be stated concretely
- `needs_check`: at least one review round has started and a missing fact could materially change the recommendation
- `conflicting`: credible sources support incompatible interpretations that matter to the recommendation
- `parked`: the direction may have value, while current priority or resource conditions favor other candidates
- `weak`: at least one targeted review round was completed and no clear, meaningful question emerged
- `excluded`: located evidence establishes a duplicate question, absence of a shared problem space, or a definite conflict with declared resource constraints

Use `status_reason` to cite the decisive facts or unresolved gap. Matrix rank alone cannot justify any status beyond `unreviewed`.

Once a review round attempts to resolve a candidate and source evidence remains unavailable or incomplete, use `needs_check` with a concrete next action. Reserve `unreviewed` for candidates that have not entered the review loop.

## Data Problems

Data-integrity failures are processing issues. Record them in `data_issue`, leave the research status as `unreviewed`, repair the source data, clear the issue, and restart the review.

## Revisions

All research statuses may be reopened. Preserve the review log so a researcher can see which evidence changed the judgment.
