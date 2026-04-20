# Host-Neutral Usage

## Goal

Use this skill in any environment, not only one agent host.

## Principle

The workflow is the stable unit. Host syntax is just the loading mechanism.

## If the Host Supports Native Skills

Load the skill using the host's own skill mechanism, then follow:

- `SKILL.md`
- `references/search-playbook.md`
- `references/workflow.md`
- `references/framing-and-theory.md`
- `references/experiment-plan.md`

## If the Host Does Not Support Native Skills

Use the skill manually:

1. Read `SKILL.md`
2. Copy the templates from `assets/templates/`
3. Run the helper scripts in `scripts/`
4. Follow the workflow sections in order

## Search Capability Mapping

Map available tools into these roles:

- `broad search`: web search, browser search, paper search APIs
- `paper metadata`: CrossRef, Semantic Scholar, arXiv, PubMed
- `citation chaining`: academic search engines, "cited by", related papers
- `code search`: GitHub search, repo search, model zoo, project pages
- `fact verification`: official docs, benchmark leaderboards, author pages, repos

## Minimum Capability Contract

To use this skill well, the host should have at least one of:

- a web search surface
- a paper database API
- a browser that can reach academic search sites

If none exists:

- say that current-literature confidence is degraded
- avoid strong claims about novelty
- use only explicit, verifiable local inputs

## Output Contract

Regardless of host, the outputs should look the same:

- search log
- paper pool
- idea matrix
- idea briefs
- experiment plan
