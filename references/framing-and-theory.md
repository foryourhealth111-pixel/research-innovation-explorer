# Framing and Theory

## Goal

Write a framework section that clarifies the idea instead of disguising it.

## Honest Framing Patterns

### 1. Shared Objective Family

Use when A and B optimize related objectives in the same output space.

Template:

```text
Define one objective J(theta; alpha, beta).
Show that alpha=1 recovers A and alpha=0 recovers B.
State the assumptions needed for the interpolation to be meaningful.
```

### 2. Controller or Gating Family

Use when A-style and B-style mechanisms can be selected or blended by a learned controller.

Template:

```text
F(x) = G(x) * F_A(x) + (1 - G(x)) * F_B(x)
```

Only use this if:

- both branches operate in compatible spaces
- the gate has a clear interpretation
- the evaluation actually tests whether the gate matters

### 3. Constraint Relaxation

Use when A and B correspond to different operating points of one constrained problem.

Template:

```text
minimize L_main + lambda * L_constraint
```

Then show which settings recover earlier methods.

### 4. Two-Stage Decomposition

Use when one method is naturally the proposal stage and the other is the refinement stage.

Template:

```text
z = T_A(x)
y = T_B(x, z)
```

This is often more honest than pretending the two parts are one symmetric fusion.

## Questions to Answer Before Claiming "A and B Are Special Cases"

- What is the common variable or state space?
- What parameter recovers A?
- What parameter recovers B?
- What assumptions are required?
- What regimes break the equivalence?
- What evidence will show the generalized form is useful in practice?

If any of these are unclear, downgrade the claim.

## Safe Language

Prefer:

- "We model A and B as limiting cases under assumptions ..."
- "We interpret the composition through a unified controller ..."
- "We instantiate the broader family with two endpoints ..."

Avoid:

- "We prove generality" when there is no proof
- "A and B naturally emerge" when the mapping is hand-built
- "Our theory strictly subsumes prior work" unless that statement is actually verified

## `alpha` and Other Fusion Parameters

Use a free parameter only if it has a concrete interpretation:

- trust in branch A versus branch B
- allocation between retrieval and generation
- precision versus coverage
- exploitation versus exploration

Do not introduce `alpha` only to make a simple merge look deep.

## Minimum Framing Package

Every shortlisted idea should state:

- the common abstraction
- the exact role of A
- the exact role of B
- the control variable or composition rule
- assumptions
- expected gains
- failure boundary
