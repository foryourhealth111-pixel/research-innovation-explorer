#!/usr/bin/env python3
"""
Build a scored pairwise idea matrix from a structured paper pool CSV.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import re
from pathlib import Path

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
}
TRUTHY = {"1", "true", "yes", "y", "open", "opensource"}
REQUIRED_COLUMNS = {
    "paper_id",
    "title",
    "task",
    "modules",
    "strengths",
    "weaknesses",
    "open_source",
}
TOKEN_PATTERN = re.compile(r"[a-z0-9][a-z0-9+\-]*")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate scored pairwise research idea candidates from a paper pool CSV."
    )
    parser.add_argument("input_csv", help="CSV file copied from assets/templates/paper-pool.csv")
    parser.add_argument(
        "--output",
        required=True,
        help="Output CSV path for the scored pairwise idea matrix",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=0.0,
        help="Drop rows below this total score after ranking (default: 0)",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=0,
        help="Keep only the top K rows after sorting; 0 keeps all rows",
    )
    return parser.parse_args()


def bool_from_text(value: str) -> bool:
    return value.strip().lower() in TRUTHY


def tokenize(value: str) -> set[str]:
    tokens = {
        token
        for token in TOKEN_PATTERN.findall(value.lower())
        if token not in STOPWORDS and len(token) > 2
    }
    return tokens


def jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(value, upper))


def first_phrase(raw_value: str, fallback: str) -> str:
    for part in re.split(r"[;,|/]", raw_value):
        cleaned = part.strip()
        if cleaned:
            return cleaned
    return fallback


def load_papers(path: Path) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - fieldnames
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise ValueError(f"Missing required columns: {missing_list}")

        papers = []
        for row in reader:
            paper_id = row.get("paper_id", "").strip()
            title = row.get("title", "").strip()
            if not paper_id or not title:
                continue
            papers.append(
                {
                    "paper_id": paper_id,
                    "title": title,
                    "task_raw": row.get("task", ""),
                    "modules_raw": row.get("modules", ""),
                    "strengths_raw": row.get("strengths", ""),
                    "weaknesses_raw": row.get("weaknesses", ""),
                    "benchmarks_raw": row.get("benchmarks", ""),
                    "venue": row.get("venue", "").strip(),
                    "year": row.get("year", "").strip(),
                    "open_source": bool_from_text(row.get("open_source", "")),
                    "task_tokens": tokenize(row.get("task", "")),
                    "module_tokens": tokenize(row.get("modules", "")),
                    "strength_tokens": tokenize(row.get("strengths", "")),
                    "weakness_tokens": tokenize(row.get("weaknesses", "")),
                    "benchmark_tokens": tokenize(row.get("benchmarks", "")),
                }
            )
        return papers


def score_pair(left: dict[str, object], right: dict[str, object]) -> dict[str, object]:
    task_overlap = jaccard(left["task_tokens"], right["task_tokens"])
    module_overlap = jaccard(left["module_tokens"], right["module_tokens"])
    module_diversity = 1.0 - module_overlap
    weakness_coverage = max(
        jaccard(left["strength_tokens"], right["weakness_tokens"]),
        jaccard(right["strength_tokens"], left["weakness_tokens"]),
    )
    benchmark_overlap = jaccard(left["benchmark_tokens"], right["benchmark_tokens"])
    open_source_bonus = 1.0 if left["open_source"] and right["open_source"] else 0.4 if left["open_source"] or right["open_source"] else 0.0
    narrative_bonus = 1.0 if task_overlap >= 0.12 and module_diversity >= 0.35 else 0.0
    redundancy_penalty = 1.0 if module_overlap >= 0.75 else 0.0
    disconnect_penalty = 1.0 if task_overlap < 0.05 and benchmark_overlap < 0.05 else 0.0

    weighted = (
        0.25 * task_overlap
        + 0.25 * module_diversity
        + 0.20 * weakness_coverage
        + 0.10 * benchmark_overlap
        + 0.10 * open_source_bonus
        + 0.10 * narrative_bonus
        - 0.15 * redundancy_penalty
        - 0.10 * disconnect_penalty
    )
    total_score = round(100 * clamp(weighted), 2)

    rationale = []
    if task_overlap >= 0.12:
        rationale.append("shared task signal")
    if module_diversity >= 0.35:
        rationale.append("different mechanism families")
    if weakness_coverage >= 0.08:
        rationale.append("one strength may cover the other's weakness")
    if benchmark_overlap >= 0.08:
        rationale.append("evaluation overlap is available")
    if open_source_bonus >= 1.0:
        rationale.append("both papers appear open-source")
    elif open_source_bonus > 0.0:
        rationale.append("partial code availability")
    if redundancy_penalty:
        rationale.append("penalty: mechanisms look too similar")
    if disconnect_penalty:
        rationale.append("penalty: task mismatch is high")

    left_task = first_phrase(left["task_raw"], "the shared task")
    left_module = first_phrase(left["modules_raw"], "paper A's mechanism")
    right_module = first_phrase(right["modules_raw"], "paper B's mechanism")
    right_weakness = first_phrase(right["weaknesses_raw"], "paper B's weak regime")
    hypothesis = (
        f"Use {left_module} from {left['paper_id']} with {right_module} from {right['paper_id']} "
        f"for {left_task}, targeting {right_weakness} as the main gain hypothesis."
    )

    return {
        "paper_a_id": left["paper_id"],
        "paper_a_title": left["title"],
        "paper_a_venue": left["venue"],
        "paper_a_year": left["year"],
        "paper_b_id": right["paper_id"],
        "paper_b_title": right["title"],
        "paper_b_venue": right["venue"],
        "paper_b_year": right["year"],
        "task_overlap": round(task_overlap, 4),
        "module_diversity": round(module_diversity, 4),
        "weakness_coverage": round(weakness_coverage, 4),
        "benchmark_overlap": round(benchmark_overlap, 4),
        "open_source_bonus": round(open_source_bonus, 4),
        "narrative_bonus": round(narrative_bonus, 4),
        "redundancy_penalty": round(redundancy_penalty, 4),
        "disconnect_penalty": round(disconnect_penalty, 4),
        "total_score": total_score,
        "rationale": "; ".join(rationale) if rationale else "manual review required",
        "hypothesis_stub": hypothesis,
    }


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        fieldnames = [
            "paper_a_id",
            "paper_a_title",
            "paper_a_venue",
            "paper_a_year",
            "paper_b_id",
            "paper_b_title",
            "paper_b_venue",
            "paper_b_year",
            "task_overlap",
            "module_diversity",
            "weakness_coverage",
            "benchmark_overlap",
            "open_source_bonus",
            "narrative_bonus",
            "redundancy_penalty",
            "disconnect_penalty",
            "total_score",
            "rationale",
            "hypothesis_stub",
        ]
    else:
        fieldnames = list(rows[0].keys())

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    input_path = Path(args.input_csv).resolve()
    output_path = Path(args.output).resolve()

    papers = load_papers(input_path)
    if len(papers) < 2:
        raise ValueError("Need at least two valid paper rows to build a pairwise matrix")

    rows = [
        score_pair(left, right)
        for left, right in itertools.combinations(papers, 2)
        if left["paper_id"] != right["paper_id"]
    ]
    rows.sort(key=lambda row: row["total_score"], reverse=True)
    rows = [row for row in rows if row["total_score"] >= args.min_score]
    if args.top_k > 0:
        rows = rows[: args.top_k]

    write_rows(output_path, rows)
    print(f"Wrote {len(rows)} candidate rows to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
