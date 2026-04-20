#!/usr/bin/env python3
"""
Build a polished Markdown research idea report from CSV artifacts.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Markdown report with visual summaries and references."
    )
    parser.add_argument("--topic", required=True, help="Report topic")
    parser.add_argument("--paper-pool", required=True, help="Path to paper_pool.csv")
    parser.add_argument("--idea-matrix", required=True, help="Path to idea_matrix.csv")
    parser.add_argument("--search-log", required=True, help="Path to search_log.csv")
    parser.add_argument("--output", required=True, help="Output Markdown path")
    parser.add_argument("--top-k", type=int, default=5, help="Top candidate rows to include")
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
            "    D --> E[Shortlist]",
            "    E --> F[Theory Framing]",
            "    F --> G[Experiment Plan]",
            "    G --> H[Markdown Report]",
            "```",
        ]
    )


def build_report(
    topic: str,
    papers: list[dict[str, str]],
    ideas: list[dict[str, str]],
    searches: list[dict[str, str]],
    top_k: int,
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
                "Task overlap is actionable",
                f"Matrix task_overlap={best.get('task_overlap', '')} and benchmark_overlap={best.get('benchmark_overlap', '')}",
                f"[{ref_a}], [{ref_b}]",
            ],
            [
                "Mechanism complementarity is real",
                f"Matrix module_diversity={best.get('module_diversity', '')}; rationale={best.get('rationale', '')}",
                f"[{ref_a}], [{ref_b}]",
            ],
            [
                "Implementation path is plausible",
                f"open_source_bonus={best.get('open_source_bonus', '')}; hypothesis={best.get('hypothesis_stub', '')}",
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
        f"# Research Innovation Report: {topic}",
        "",
        "> Generated from the search log, paper pool, and idea matrix. Refine the narrative before final use.",
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
        "## Recommended Direction",
        "",
        "Use the highest-scoring candidate only as the current best lead, not as a final claim of novelty.",
        "",
        f"- Lead hypothesis: {summary_text}",
        "",
        "## Analysis Basis",
        "",
        "Every major claim in the report should trace back to either logged searches, paper metadata, or matrix-derived evidence.",
        "",
        markdown_table(evidence_rows, ["Claim", "Basis", "Support"]),
        "",
        "## Detailed Analysis",
        "",
        "### Why the top candidate is interesting",
        "",
        "- Explain the shared task and why the evaluation space is meaningful.",
        "- Explain the complementary mechanisms in concrete architectural terms.",
        "- Explain which weak regime the combination is meant to address.",
        "",
        "### What could invalidate it",
        "",
        "- Similar prior work discovered during a novelty check.",
        "- Benchmark overlap that looks stronger on paper than in practice.",
        "- Missing code, hidden training cost, or data mismatch.",
        "",
        "### What to verify next",
        "",
        "- Run a dedicated prior-art search against the exact combination claim.",
        "- Confirm the baselines and evaluation protocol.",
        "- Draft the ablations that could falsify the mechanism story.",
        "",
        "## References",
        "",
        *references,
        "",
        "## Notes",
        "",
        "- If the renderer does not support Mermaid, keep the Markdown tables and replace Mermaid blocks with static images or plain-text summaries.",
        "- Before publishing, add any missing DOI, arXiv ID, or canonical project URL.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    topic = args.topic.strip()
    paper_pool = read_csv(Path(args.paper_pool).resolve())
    idea_matrix = read_csv(Path(args.idea_matrix).resolve())
    search_log = read_csv(Path(args.search_log).resolve())
    report = build_report(topic, paper_pool, idea_matrix, search_log, args.top_k)

    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote Markdown report to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
