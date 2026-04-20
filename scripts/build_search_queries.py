#!/usr/bin/env python3
"""
Generate a structured literature search query pack from a topic and seed keywords.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate broad and deep literature search queries for research idea exploration."
    )
    parser.add_argument("--topic", required=True, help="Primary research topic")
    parser.add_argument(
        "--keywords",
        default="",
        help="Comma-separated method, task, benchmark, or domain keywords",
    )
    parser.add_argument(
        "--output",
        help="Optional path to save the query pack as JSON; prints to stdout if omitted",
    )
    return parser.parse_args()


def normalize_keywords(raw_keywords: str) -> list[str]:
    items = []
    for chunk in raw_keywords.split(","):
        text = re.sub(r"\s+", " ", chunk.strip())
        if text and text not in items:
            items.append(text)
    return items


def join_terms(topic: str, keywords: list[str]) -> str:
    terms = [topic] + keywords
    return " ".join(term for term in terms if term)


def build_query_pack(topic: str, keywords: list[str]) -> dict[str, object]:
    core = join_terms(topic, keywords)
    keyword_clause = " OR ".join(f"\"{keyword}\"" for keyword in keywords) if keywords else f"\"{topic}\""
    broad_query = f"\"{topic}\" recent papers"
    method_query = f"({keyword_clause}) AND \"{topic}\""

    return {
        "topic": topic,
        "keywords": keywords,
        "query_groups": [
            {
                "name": "broad-topic-scan",
                "purpose": "Find recent surveys, strong papers, and major threads.",
                "queries": [
                    broad_query,
                    f"{core} survey OR review OR benchmark",
                    f"{core} state of the art",
                ],
            },
            {
                "name": "method-scan",
                "purpose": "Map concrete method families and strong baselines.",
                "queries": [
                    method_query,
                    f"{core} method comparison",
                    f"{core} open-source code github",
                ],
            },
            {
                "name": "benchmark-and-data-scan",
                "purpose": "Find shared evaluation surfaces and reproducible setups.",
                "queries": [
                    f"{core} benchmark dataset leaderboard",
                    f"{core} evaluation protocol",
                    f"{core} github benchmark",
                ],
            },
            {
                "name": "novelty-and-prior-art-check",
                "purpose": "Search for similar compositions, precursor work, and overlap risk.",
                "queries": [
                    f"{core} hybrid fusion unified framework",
                    f"{core} combination of methods",
                    f"{core} special case general framework",
                ],
            },
            {
                "name": "negative-evidence-and-failure-check",
                "purpose": "Search for failed replications, limitations, and caveats.",
                "queries": [
                    f"{core} limitations failure analysis",
                    f"{core} ablation weakness",
                    f"{core} replication issue",
                ],
            },
            {
                "name": "citation-chaining-prompts",
                "purpose": "Use on a promising seed paper to find its neighborhood.",
                "queries": [
                    f"papers citing <seed-paper-title> {topic}",
                    f"related work to <seed-paper-title> {topic}",
                    f"similar papers to <seed-paper-title> {topic}",
                ],
            },
        ],
        "source_hints": [
            "general web search",
            "Google Scholar or equivalent academic search",
            "Semantic Scholar",
            "arXiv",
            "CrossRef",
            "PubMed when biomedical",
            "official paper code repositories",
            "GitHub repository search",
        ],
    }


def main() -> int:
    args = parse_args()
    topic = re.sub(r"\s+", " ", args.topic.strip())
    if not topic:
        raise ValueError("Topic must not be empty")
    keywords = normalize_keywords(args.keywords)
    pack = build_query_pack(topic, keywords)
    rendered = json.dumps(pack, ensure_ascii=False, indent=2)

    if args.output:
        output_path = Path(args.output).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")
        print(f"Wrote query pack to {output_path}")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
