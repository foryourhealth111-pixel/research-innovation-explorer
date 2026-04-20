# Experiment Plan

## Goal

Show that the idea is more than a cosmetic combination.

## Baseline Ladder

Always include:

1. method A
2. method B
3. naive composition baseline
4. proposed method

Optional:

5. strongest recent third-party baseline
6. lightweight or cheaper variant

## Ablation Checklist

Use only the ablations that match the mechanism:

- remove the A-style branch
- remove the B-style branch
- replace learned fusion with fixed fusion
- freeze the controller or gate
- sweep `alpha` or other mixture weights
- remove the part that supposedly addresses the predicted weak regime

## What to Measure

Measure more than one axis when possible:

- primary task metric
- robustness or stress metric
- latency or throughput
- parameter count or memory cost
- training stability

## `alpha` Sweep Rules

If the idea uses a fusion weight:

- sweep the full range, not one hand-picked midpoint
- report whether the middle region really beats both endpoints
- report when the interpolation collapses to one endpoint

This sweep is evidence only when the parameter has a real semantic meaning.

## Failure Analysis

Reserve at least one subsection for failure cases:

- where A still wins
- where B still wins
- where the combined method adds cost without benefit
- where the framing assumptions break

## Promotion Rule

Promote the idea from shortlist to implementation only if at least one is true:

- it beats both A and B on the target regime
- it materially improves the quality-cost tradeoff
- it wins on the exact failure mode the hypothesis predicted

If none of these is true, kill or redesign the idea.
