#!/usr/bin/env python3
"""
Generate publication-style post-research figures from paper-pool and idea-matrix CSV artifacts.
"""

from __future__ import annotations

import argparse
import json
import re
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


REQUIRED_PAPER_COLUMNS = {"paper_id", "title"}
REQUIRED_IDEA_COLUMNS = {"paper_a_id", "paper_b_id", "total_score"}
THEME_FIELD_ORDER = ("tags", "modules", "task", "venue")
SPLIT_PATTERN = re.compile(r"[;,|/]")
SCORE_METRICS = [
    ("task_overlap", "Task match", 1.0),
    ("module_diversity", "Module diversity", 1.0),
    ("weakness_coverage", "Weakness coverage", 1.0),
    ("benchmark_overlap", "Benchmark overlap", 1.0),
    ("open_source_bonus", "Open-source readiness", 1.0),
    ("narrative_bonus", "Narrative sharpness", 1.0),
    ("total_score", "Total score", 100.0),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create literature heatmap, candidate scoring heatmap, and analysis-panel figures."
    )
    parser.add_argument("--paper-pool", required=True, help="Path to paper_pool.csv")
    parser.add_argument("--idea-matrix", required=True, help="Path to idea_matrix.csv")
    parser.add_argument("--output-dir", required=True, help="Directory for generated figures and data")
    parser.add_argument("--topic", default="Research landscape", help="Figure title topic")
    parser.add_argument("--prefix", default="research", help="Output filename prefix")
    parser.add_argument("--top-k", type=int, default=12, help="Top candidate rows for the scoring figure")
    parser.add_argument(
        "--theme-field",
        choices=["auto", "tags", "modules", "task", "venue"],
        default="auto",
        help="Paper-pool column used to group papers for the literature heatmap",
    )
    parser.add_argument(
        "--formats",
        default="png,pdf",
        help="Comma-separated output formats, for example: png,pdf,svg",
    )
    parser.add_argument("--dpi", type=int, default=300, help="Raster export DPI")
    return parser.parse_args()


def load_csv(path: Path, required_columns: set[str], label: str) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = required_columns - set(frame.columns)
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(f"{label} is missing required columns: {missing_list}")
    return frame


def parse_formats(raw: str) -> list[str]:
    formats = [part.strip().lstrip(".").lower() for part in raw.split(",") if part.strip()]
    if not formats:
        raise ValueError("At least one export format is required")
    return formats


def first_token(value: object, fallback: str) -> str:
    text = "" if pd.isna(value) else str(value).strip()
    if not text:
        return fallback
    for part in SPLIT_PATTERN.split(text):
        cleaned = part.strip()
        if cleaned:
            return cleaned
    return fallback


def compact_label(value: str, max_chars: int = 18) -> str:
    text = value.replace("_", " ").replace("-", " ").strip()
    text = re.sub(r"\s+", " ", text)
    if not text:
        return "Unknown"
    title = text.title()
    return title if len(title) <= max_chars else title[: max_chars - 1].rstrip() + "."


def wrap_label(value: object, width: int = 13, max_lines: int = 2) -> str:
    text = "" if pd.isna(value) else str(value).strip()
    if not text:
        return "Unknown"
    lines = textwrap.wrap(text, width=width, break_long_words=False) or [text]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: max(1, width - 1)].rstrip() + "."
    return "\n".join(lines)


def candidate_label(row: pd.Series) -> str:
    return f"{row.get('paper_a_id', '')} + {row.get('paper_b_id', '')}"


def setup_style() -> None:
    sns.set_theme(style="ticks", context="paper", font_scale=1.05)
    sns.set_palette("colorblind")
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans", "Arial", "Liberation Sans"],
            "axes.unicode_minus": False,
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def choose_theme_field(papers: pd.DataFrame, requested: str) -> str:
    if requested != "auto":
        if requested not in papers.columns:
            raise ValueError(f"Requested theme field is not present in paper pool: {requested}")
        return requested
    for field in THEME_FIELD_ORDER:
        if field in papers.columns and papers[field].fillna("").astype(str).str.strip().any():
            return field
    return "paper_id"


def build_theme_map(papers: pd.DataFrame, theme_field: str) -> dict[str, str]:
    theme_map: dict[str, str] = {}
    for _, row in papers.iterrows():
        paper_id = str(row["paper_id"]).strip()
        if not paper_id:
            continue
        raw_theme = row.get(theme_field, paper_id)
        theme_map[paper_id] = compact_label(first_token(raw_theme, paper_id))
    return theme_map


def build_theme_matrix(ideas: pd.DataFrame, theme_map: dict[str, str]) -> pd.DataFrame:
    frame = ideas.copy()
    frame["theme_a"] = frame["paper_a_id"].astype(str).map(theme_map).fillna("Unknown")
    frame["theme_b"] = frame["paper_b_id"].astype(str).map(theme_map).fillna("Unknown")
    frame["total_score"] = pd.to_numeric(frame["total_score"], errors="coerce")
    frame = frame.dropna(subset=["total_score"])
    if frame.empty:
        raise ValueError("Idea matrix has no numeric total_score values")

    grouped = frame.groupby(["theme_a", "theme_b"], as_index=False)["total_score"].mean()
    directed = grouped.pivot(index="theme_a", columns="theme_b", values="total_score")
    themes = sorted(set(grouped["theme_a"]) | set(grouped["theme_b"]))
    directed = directed.reindex(index=themes, columns=themes)
    symmetric = directed.copy()

    for row in themes:
        for col in themes:
            values = []
            if pd.notna(directed.loc[row, col]):
                values.append(float(directed.loc[row, col]))
            if pd.notna(directed.loc[col, row]):
                values.append(float(directed.loc[col, row]))
            symmetric.loc[row, col] = sum(values) / len(values) if values else float("nan")
    return symmetric


def build_scoring_matrix(ideas: pd.DataFrame, top_k: int) -> pd.DataFrame:
    frame = ideas.copy()
    frame["total_score"] = pd.to_numeric(frame["total_score"], errors="coerce")
    frame = frame.dropna(subset=["total_score"]).sort_values("total_score", ascending=False)
    if top_k > 0:
        frame = frame.head(top_k)
    if frame.empty:
        raise ValueError("Idea matrix has no candidate rows after filtering")

    score_data = pd.DataFrame(index=[candidate_label(row) for _, row in frame.iterrows()])
    for name, label, scale in SCORE_METRICS:
        if name not in frame.columns:
            continue
        values = pd.to_numeric(frame[name], errors="coerce").fillna(0.0) / scale
        score_data[label] = values.clip(lower=0.0, upper=1.0).to_list()
    if score_data.empty:
        raise ValueError("Idea matrix does not contain usable scoring columns")
    return score_data


def add_panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(
        -0.12,
        1.08,
        label,
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        va="top",
        ha="left",
    )


def save_figure(fig: plt.Figure, output_dir: Path, stem: str, formats: list[str], dpi: int) -> list[str]:
    paths = []
    for fmt in formats:
        path = output_dir / f"{stem}.{fmt}"
        fig.savefig(path, bbox_inches="tight", dpi=dpi)
        paths.append(str(path))
    plt.close(fig)
    return paths


def make_literature_heatmap(
    matrix: pd.DataFrame,
    topic: str,
    output_dir: Path,
    prefix: str,
    formats: list[str],
    dpi: int,
) -> dict[str, object]:
    width = max(4.0, min(10.0, 0.55 * len(matrix.columns) + 2.3))
    height = max(3.6, min(9.0, 0.48 * len(matrix.index) + 1.8))
    fig, ax = plt.subplots(figsize=(width, height))
    sns.heatmap(
        matrix,
        cmap="viridis",
        annot=len(matrix.index) <= 12 and len(matrix.columns) <= 12,
        fmt=".1f",
        linewidths=0.5,
        linecolor="white",
        cbar_kws={"label": "Mean candidate score"},
        ax=ax,
    )
    ax.set_title(f"{topic}: literature interaction heatmap", fontweight="bold", pad=12, fontsize=10)
    ax.set_xlabel("Paper theme B", fontsize=9)
    ax.set_ylabel("Paper theme A", fontsize=9)
    ax.set_xticklabels([wrap_label(label.get_text()) for label in ax.get_xticklabels()], rotation=35, ha="right")
    ax.set_yticklabels([wrap_label(label.get_text(), width=16) for label in ax.get_yticklabels()], rotation=0)
    ax.tick_params(axis="both", labelsize=7)
    fig.tight_layout()

    data_path = output_dir / f"{prefix}_literature_heatmap_data.csv"
    matrix.to_csv(data_path)
    paths = save_figure(fig, output_dir, f"{prefix}_literature_heatmap", formats, dpi)
    return {"figure_paths": paths, "data_path": str(data_path)}


def make_candidate_scoring_heatmap(
    score_data: pd.DataFrame,
    topic: str,
    output_dir: Path,
    prefix: str,
    formats: list[str],
    dpi: int,
) -> dict[str, object]:
    height = max(3.2, min(8.5, 0.38 * len(score_data.index) + 1.6))
    fig, ax = plt.subplots(figsize=(7.2, height))
    sns.heatmap(
        score_data,
        cmap="mako",
        vmin=0.0,
        vmax=1.0,
        annot=True,
        fmt=".2f",
        linewidths=0.5,
        linecolor="white",
        cbar_kws={"label": "Normalized score"},
        annot_kws={"fontsize": 7},
        ax=ax,
    )
    ax.set_title(f"{topic}: shortlisted candidate scoring", fontweight="bold", pad=12, fontsize=10)
    ax.set_xlabel("Scoring dimension", fontsize=9)
    ax.set_ylabel("Candidate", fontsize=9)
    ax.set_xticklabels([wrap_label(label.get_text(), width=12) for label in ax.get_xticklabels()], rotation=28, ha="right")
    ax.tick_params(axis="x", labelsize=7)
    ax.tick_params(axis="y", rotation=0, labelsize=8)
    fig.tight_layout()

    data_path = output_dir / f"{prefix}_candidate_scoring_data.csv"
    score_data.to_csv(data_path)
    paths = save_figure(fig, output_dir, f"{prefix}_candidate_scoring_heatmap", formats, dpi)
    return {"figure_paths": paths, "data_path": str(data_path)}


def make_analysis_panel(
    papers: pd.DataFrame,
    ideas: pd.DataFrame,
    topic: str,
    output_dir: Path,
    prefix: str,
    formats: list[str],
    dpi: int,
) -> dict[str, object]:
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.8))
    ax_year, ax_venue, ax_score, ax_top = axes.flatten()

    if "year" in papers.columns:
        years = papers["year"].fillna("Unknown").astype(str).str.strip().replace("", "Unknown")
        year_counts = years.value_counts().sort_index()
    else:
        year_counts = pd.Series({"Unknown": len(papers)})
    year_counts.plot(kind="bar", ax=ax_year, color="#4C78A8", width=0.8)
    ax_year.set_title("Paper years", fontsize=9)
    ax_year.set_xlabel("")
    ax_year.set_ylabel("Count")
    ax_year.tick_params(axis="x", rotation=35)
    add_panel_label(ax_year, "A")

    venues = (
        papers.get("venue", pd.Series(["Unknown"] * len(papers)))
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
    )
    venue_counts = venues.value_counts().head(8).sort_values()
    venue_counts.plot(kind="barh", ax=ax_venue, color="#59A14F")
    ax_venue.set_title("Top venues", fontsize=9)
    ax_venue.set_xlabel("Count")
    ax_venue.set_ylabel("")
    add_panel_label(ax_venue, "B")

    scores = pd.to_numeric(ideas["total_score"], errors="coerce").dropna()
    if len(scores) > 1:
        ax_score.hist(scores, bins=min(12, max(4, int(len(scores) ** 0.5))), color="#F28E2B", alpha=0.85)
    elif len(scores) == 1:
        ax_score.bar(["candidate"], [scores.iloc[0]], color="#F28E2B")
    else:
        ax_score.text(0.5, 0.5, "No scores", ha="center", va="center")
    ax_score.set_title("Candidate score distribution", fontsize=9)
    ax_score.set_xlabel("Total score")
    ax_score.set_ylabel("Count")
    add_panel_label(ax_score, "C")

    top = ideas.copy()
    top["total_score"] = pd.to_numeric(top["total_score"], errors="coerce")
    top = top.dropna(subset=["total_score"]).sort_values("total_score", ascending=False).head(8)
    if not top.empty:
        labels = [candidate_label(row) for _, row in top.iloc[::-1].iterrows()]
        ax_top.barh(labels, top["total_score"].iloc[::-1], color="#B07AA1")
    else:
        ax_top.text(0.5, 0.5, "No candidates", ha="center", va="center")
    ax_top.set_title("Top candidate scores", fontsize=9)
    ax_top.set_xlabel("Total score")
    ax_top.set_ylabel("")
    add_panel_label(ax_top, "D")

    fig.suptitle(f"{topic}: research artifact analysis", fontweight="bold", y=1.02, fontsize=11)
    fig.tight_layout()
    paths = save_figure(fig, output_dir, f"{prefix}_analysis_panel", formats, dpi)
    return {"figure_paths": paths}


def main() -> int:
    args = parse_args()
    paper_pool_path = Path(args.paper_pool).resolve()
    idea_matrix_path = Path(args.idea_matrix).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    formats = parse_formats(args.formats)

    setup_style()
    papers = load_csv(paper_pool_path, REQUIRED_PAPER_COLUMNS, "paper pool")
    ideas = load_csv(idea_matrix_path, REQUIRED_IDEA_COLUMNS, "idea matrix")
    theme_field = choose_theme_field(papers, args.theme_field)
    theme_map = build_theme_map(papers, theme_field)
    theme_matrix = build_theme_matrix(ideas, theme_map)
    score_data = build_scoring_matrix(ideas, args.top_k)

    outputs = {
        "literature_heatmap": make_literature_heatmap(
            theme_matrix, args.topic, output_dir, args.prefix, formats, args.dpi
        ),
        "candidate_scoring_heatmap": make_candidate_scoring_heatmap(
            score_data, args.topic, output_dir, args.prefix, formats, args.dpi
        ),
        "analysis_panel": make_analysis_panel(
            papers, ideas, args.topic, output_dir, args.prefix, formats, args.dpi
        ),
    }

    manifest = {
        "inputs": {
            "paper_pool": str(paper_pool_path),
            "idea_matrix": str(idea_matrix_path),
        },
        "records": {
            "paper_count": int(len(papers)),
            "candidate_count": int(len(ideas)),
            "theme_count": int(len(theme_matrix.index)),
            "top_k": int(args.top_k),
        },
        "style_contract": {
            "purpose": "publication-style post-research figures",
            "theme_field": theme_field,
            "formats": formats,
            "dpi": args.dpi,
            "palette": "colorblind/sequential",
        },
        "outputs": outputs,
    }
    manifest_path = output_dir / f"{args.prefix}_figure_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote research figure bundle to {output_dir}")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
