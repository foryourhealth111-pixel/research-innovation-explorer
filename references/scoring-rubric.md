# Scoring Rubric

## Use This Rubric

Use this rubric after `build_idea_matrix.py` to separate promising pairings from noisy ones.

## Core Dimensions

Score each dimension from 0 to 5.

| Dimension | What to ask | Weight |
| --- | --- | --- |
| Task overlap | Do both papers operate on the same or adjacent problem? | 0.20 |
| Mechanism complementarity | Are the mechanisms meaningfully different? | 0.20 |
| Weakness coverage | Does one paper's strength plausibly address the other's weak regime? | 0.20 |
| Implementation tractability | Can the pair be built with available code, compute, and data? | 0.15 |
| Evaluation availability | Can the pair be tested on a shared benchmark stack? | 0.10 |
| Narrative strength | Can the contribution be expressed as one sharp hypothesis? | 0.10 |
| Novelty headroom | Is there still room after accounting for recent related work? | 0.05 |

## Penalties

Subtract penalties when these apply:

- `-2`: same mechanism family with mostly superficial changes
- `-2`: no code or realistic reproduction path
- `-1`: evaluation stack mismatch is painful but still solvable
- `-2`: no honest framing path beyond direct stitching

## Fast Prune Rules

Kill a candidate immediately if:

- the combined claim depends on unavailable infrastructure
- the central evaluation cannot be defined clearly
- the only plausible story is benchmark cherry-picking
- the control variable cannot be described in one sentence

## Shortlist Bands

- `4.2-5.0`: strong candidate, write a full brief
- `3.5-4.1`: keep for secondary review
- `2.8-3.4`: only keep if there is strategic value or an unusually easy implementation path
- `<2.8`: drop

## What Usually Survives

Strong candidates tend to look like:

- same task, different mechanism families
- one method expands coverage, one improves precision or efficiency
- both have code and compatible evaluation
- one simple control variable explains the combination

## What Usually Fails

Weak candidates tend to look like:

- same task, same module, new wording only
- no shared evaluation space
- three different ideas forced into one narrative
- theoretical language added after the fact without a real abstraction
