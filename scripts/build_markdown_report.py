#!/usr/bin/env python3
"""Build a Markdown matrix-overview scaffold from CSV artifacts."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Markdown matrix-overview scaffold with visuals and references."
    )
    parser.add_argument("--topic", required=True, help="Report topic")
    parser.add_argument("--paper-pool", required=True, help="Path to paper_pool.csv")
    parser.add_argument("--idea-matrix", required=True, help="Path to idea_matrix.csv")
    parser.add_argument("--search-log", required=True, help="Path to search_log.csv")
    parser.add_argument("--output", required=True, help="Output Markdown path")
    parser.add_argument("--top-k", type=int, default=5, help="Top candidate rows to include")
    parser.add_argument(
        "--figure-dir",
        default="",
        help="Optional directory produced by scripts/build_research_figures.py",
    )
    parser.add_argument(
        "--figure-prefix",
        default="research",
        help="Filename prefix used by scripts/build_research_figures.py",
    )
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def normalize_url(url: str) -> str:
    text = (url or "").strip()
    return text if text else "URL unavailable"


def markdown_table(rows: list[list[str]], headers: list[str]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        safe = [cell.replace("\n", " ").replace("|", "\\|") for cell in row]
        lines.append("| " + " | ".join(safe) + " |")
    return "\n".join(lines)


def build_reference_map(papers: list[dict[str, str]]) -> tuple[dict[str, str], list[str]]:
    ref_map: dict[str, str] = {}
    refs: list[str] = []
    for idx, paper in enumerate(papers, start=1):
        ref_id = f"R{idx}"
        paper_id = paper.get("paper_id", "").strip()
        ref_map[paper_id] = ref_id
        title = paper.get("title", "").strip() or "Untitled paper"
        venue = paper.get("venue", "").strip() or "Venue unavailable"
        year = paper.get("year", "").strip() or "n.d."
        refs.append(f"- [{ref_id}] {title}. {venue} ({year}). {normalize_url(paper.get('url', ''))}")
    return ref_map, refs


def venue_pie_block(papers: list[dict[str, str]]) -> str:
    counter = Counter((paper.get("venue", "").strip() or "Unknown") for paper in papers)
    lines = ["```mermaid", "pie showData", '    title Paper Pool by Venue']
    for venue, count in counter.most_common(6):
        lines.append(f'    "{venue}" : {count}')
    lines.append("```")
    return "\n".join(lines)


def workflow_mermaid() -> str:
    return "\n".join(
        [
            "```mermaid",
            "flowchart LR",
            "    A[Search Pass] --> B[Paper Pool]",
            "    B --> C[Capability Decomposition]",
            "    C --> D[Idea Matrix]",
            "    D --> E[Review Queue]",
            "    E --> F[Evidence Review]",
            "    F --> G[Candidate Landscape]",
            "```",
        ]
    )


def figure_links(figure_dir: str, figure_prefix: str, output_path: Path) -> list[str]:
    if not figure_dir:
        return []

    directory = Path(figure_dir).resolve()
    expected = [
        ("Literature interaction heatmap", f"{figure_prefix}_literature_heatmap.png"),
        ("Candidate scoring heatmap", f"{figure_prefix}_candidate_scoring_heatmap.png"),
        ("Research artifact analysis panel", f"{figure_prefix}_analysis_panel.png"),
    ]
    links = []
    for title, filename in expected:
        path = directory / filename
        if not path.exists():
            continue
        try:
            link = path.relative_to(output_path.parent.resolve()).as_posix()
        except ValueError:
            link = path.as_posix()
        links.extend([f"### {title}", "", f"![{title}]({link})", ""])
    return links


def build_report(
    topic: str,
    papers: list[dict[str, str]],
    ideas: list[dict[str, str]],
    searches: list[dict[str, str]],
    top_k: int,
    post_research_figure_links: list[str],
) -> str:
    ideas_sorted = sorted(
        ideas,
        key=lambda row: float(row.get("total_score", "0") or "0"),
        reverse=True,
    )
    top_ideas = ideas_sorted[:top_k]
    ref_map, references = build_reference_map(papers)

    search_rows = [
        [
            row.get("date", ""),
            row.get("query", ""),
            row.get("source", ""),
            row.get("reason", ""),
            row.get("key_findings", ""),
        ]
        for row in searches[:8]
    ]
    candidate_rows = []
    for idx, row in enumerate(top_ideas, start=1):
        ref_a = ref_map.get(row.get("paper_a_id", "").strip(), "?")
        ref_b = ref_map.get(row.get("paper_b_id", "").strip(), "?")
        candidate_rows.append(
            [
                str(idx),
                f"{row.get('paper_a_id', '')} + {row.get('paper_b_id', '')}",
                row.get("total_score", ""),
                row.get("rationale", ""),
                f"[{ref_a}], [{ref_b}]",
            ]
        )

    evidence_rows = []
    if top_ideas:
        best = top_ideas[0]
        ref_a = ref_map.get(best.get("paper_a_id", "").strip(), "?")
        ref_b = ref_map.get(best.get("paper_b_id", "").strip(), "?")
        evidence_rows = [
            [
                "Task-overlap screening signal",
                f"Matrix task_overlap={best.get('task_overlap', '')} and benchmark_overlap={best.get('benchmark_overlap', '')}; verify against the papers",
                f"[{ref_a}], [{ref_b}]",
            ],
            [
                "Mechanism-diversity screening signal",
                f"Matrix module_diversity={best.get('module_diversity', '')}; source review must establish any functional relationship",
                f"[{ref_a}], [{ref_b}]",
            ],
            [
                "Open-source screening signal",
                f"open_source_bonus={best.get('open_source_bonus', '')}; inspect code, data, compute, and integration requirements before judging friction",
                f"[{ref_a}], [{ref_b}]",
            ],
            [
                "Novelty still needs explicit challenge",
                "Use the search log and a dedicated prior-art check before making any strong novelty claim.",
                "search-log",
            ],
        ]
    else:
        evidence_rows = [["No candidate available", "Populate idea_matrix.csv first.", "n/a"]]

    summary_text = (
        top_ideas[0].get("hypothesis_stub", "Populate the artifacts and regenerate this report.")
        if top_ideas
        else "Populate the artifacts and regenerate this report."
    )

    lines = [
        f"# Research Candidate Matrix Overview: {topic}",
        "",
        "> Matrix-overview scaffold generated from the search log, paper pool, and idea matrix. Matrix scores are review-priority signals. Add source-based candidate reviews before making research recommendations.",
        "",
        "## Executive Summary",
        "",
        summary_text,
        "",
        "## Visual Overview",
        "",
        workflow_mermaid(),
        "",
        venue_pie_block(papers),
        "",
        *(
            [
                "## Post-Research Figures",
                "",
                "These static figures summarize the literature landscape, scoring evidence, and artifact distribution from the generated CSVs.",
                "",
                *post_research_figure_links,
            ]
            if post_research_figure_links
            else []
        ),
        "## Search Strategy",
        "",
        "The analysis used a search-first workflow and logged the major queries that shaped the paper pool and later novelty checks.",
        "",
        markdown_table(
            search_rows or [["n/a", "No logged searches yet", "n/a", "n/a", "n/a"]],
            ["Date", "Query", "Source", "Reason", "Key Findings"],
        ),
        "",
        "## Candidate Landscape",
        "",
        markdown_table(
            candidate_rows or [["1", "No candidates yet", "0", "Populate idea_matrix.csv", "n/a"]],
            ["Rank", "Candidate", "Score", "Why It Survived", "Refs"],
        ),
        "",
        "## Review Priority",
        "",
        "Use the highest-scoring candidate as the next matrix-derived review priority. Its research status remains unreviewed until source evidence is recorded.",
        "",
        f"- Lead hypothesis: {summary_text}",
        "",
        "## Analysis Basis",
        "",
        "The rows below explain matrix screening signals. Replace them with located source facts and linked agent inferences during candidate review.",
        "",
        markdown_table(evidence_rows, ["Claim", "Basis", "Support"]),
        "",
        "## Detailed Analysis",
        "",
        "### Why the highest-ranked row entered the review queue",
        "",
        "- Verify the shared task and evaluation setting against source material.",
        "- Review both A-to-B and B-to-A directions.",
        "- Record any mechanism relationship as an inference linked to observed facts.",
        "",
        "### What could invalidate it",
        "",
        "- Similar prior work discovered during a novelty check.",
        "- Benchmark overlap that looks stronger on paper than in practice.",
        "- Missing code, hidden training cost, or data mismatch.",
        "",
        "### What to verify next",
        "",
        "- Identify the single uncertainty most likely to change the recommendation.",
        "- Perform one targeted source, repository, or benchmark check.",
        "- Add status, confidence, evidence, and a concrete next check using candidate-review.yaml.",
        "",
        "## References",
        "",
        *references,
        "",
        "## Notes",
        "",
        "- If the renderer does not support Mermaid, keep the Markdown tables and replace Mermaid blocks with static images or plain-text summaries.",
        "- Before publishing, add any missing DOI, arXiv ID, or canonical project URL.",
        "- This script does not read candidate-review.yaml; merge reviewed evidence into the final candidate landscape manually.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    topic = args.topic.strip()
    paper_pool = read_csv(Path(args.paper_pool).resolve())
    idea_matrix = read_csv(Path(args.idea_matrix).resolve())
    search_log = read_csv(Path(args.search_log).resolve())
    output_path = Path(args.output).resolve()
    figures = figure_links(args.figure_dir, args.figure_prefix, output_path)
    report = build_report(topic, paper_pool, idea_matrix, search_log, args.top_k, figures)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote Markdown report to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
