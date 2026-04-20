from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_ROOT = ROOT / "assets" / "examples" / "llm-training"
DATA_DIR = EXAMPLE_ROOT / "data"

THEME_ORDER = [
    "MoE / Sparse Base Models",
    "Synthetic Alignment Data",
    "Post-training & Alignment",
    "Open Pretraining",
    "Reasoning RL",
    "Data Governance",
    "Test-time Memory",
    "Sparse Long-context Attention",
    "Self-rewarding & Judge",
    "Long-context Scaling",
    "Efficient Sequence Architectures",
    "Efficient Linear Attention",
    "Efficient Dense Architectures",
]

THEME_DISPLAY = {
    "MoE / Sparse Base Models": "MoE",
    "Synthetic Alignment Data": "Synth Align",
    "Post-training & Alignment": "Post Align",
    "Open Pretraining": "Pretrain",
    "Reasoning RL": "Reason RL",
    "Data Governance": "Data Gov",
    "Test-time Memory": "TT Memory",
    "Sparse Long-context Attention": "Sparse LC Attn",
    "Self-rewarding & Judge": "Self-Reward",
    "Long-context Scaling": "LC Scaling",
    "Efficient Sequence Architectures": "Seq Arch",
    "Efficient Linear Attention": "Linear Attn",
    "Efficient Dense Architectures": "Dense Arch",
}

THEME_MAP = {
    "A01": "Open Pretraining",
    "A02": "Open Pretraining",
    "A03": "Open Pretraining",
    "A04": "Efficient Dense Architectures",
    "A05": "Data Governance",
    "A06": "Data Governance",
    "A07": "Synthetic Alignment Data",
    "A08": "MoE / Sparse Base Models",
    "A09": "MoE / Sparse Base Models",
    "A10": "MoE / Sparse Base Models",
    "B01": "Post-training & Alignment",
    "B02": "Post-training & Alignment",
    "B03": "Self-rewarding & Judge",
    "B04": "Self-rewarding & Judge",
    "B05": "Self-rewarding & Judge",
    "B06": "Reasoning RL",
    "B07": "Reasoning RL",
    "C01": "Long-context Scaling",
    "C02": "Test-time Memory",
    "C03": "Test-time Memory",
    "D01": "Efficient Sequence Architectures",
    "D02": "Efficient Sequence Architectures",
    "D03": "Sparse Long-context Attention",
    "D04": "Efficient Linear Attention",
}

SHORTLIST_MATRIX = pd.DataFrame(
    {
        "Direction": [
            "LongRoPE + NSA",
            "LongRoPE + Kimi Linear",
            "Magpie + Meta-Rewarding",
            "Process Reward + RLVR",
            "ATLAS + NSA",
        ],
        "Novelty Space": [4.2, 3.8, 3.0, 2.8, 4.0],
        "Implementation Feasibility": [4.4, 3.8, 3.9, 3.1, 2.6],
        "Evaluation Clarity": [4.7, 4.4, 4.2, 4.4, 3.8],
        "Open-source Readiness": [4.5, 3.8, 4.0, 3.2, 2.7],
        "Narrative Sharpness": [4.5, 4.1, 4.0, 4.3, 4.1],
    }
).set_index("Direction")


def setup_style() -> None:
    sns.set_theme(style="whitegrid", context="talk")
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Liberation Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 200


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    paper_pool = pd.read_csv(DATA_DIR / "paper_pool.csv")
    idea_matrix = pd.read_csv(DATA_DIR / "idea_matrix_full.csv")
    return paper_pool, idea_matrix


def make_theme_interaction_heatmap(idea_matrix: pd.DataFrame) -> None:
    frame = idea_matrix.copy()
    frame["theme_a"] = frame["paper_a_id"].map(THEME_MAP)
    frame["theme_b"] = frame["paper_b_id"].map(THEME_MAP)
    frame = frame.dropna(subset=["theme_a", "theme_b"])

    pivot = (
        frame.groupby(["theme_a", "theme_b"])["total_score"]
        .mean()
        .reset_index()
        .pivot(index="theme_a", columns="theme_b", values="total_score")
    )
    pivot = pivot.reindex(index=THEME_ORDER, columns=THEME_ORDER)

    symmetric = pivot.copy()
    for row in THEME_ORDER:
        for col in THEME_ORDER:
            left = pivot.loc[row, col] if row in pivot.index and col in pivot.columns else None
            right = pivot.loc[col, row] if col in pivot.index and row in pivot.columns else None
            values = [value for value in [left, right] if pd.notna(value)]
            symmetric.loc[row, col] = sum(values) / len(values) if values else None

    fig, ax = plt.subplots(figsize=(15, 10.5))
    sns.heatmap(
        symmetric,
        cmap="YlOrRd",
        annot=True,
        fmt=".1f",
        linewidths=0.6,
        linecolor="white",
        cbar_kws={"label": "Average candidate score"},
        ax=ax,
    )
    ax.set_title(
        "LLM Training Theme Interaction Matrix",
        pad=16,
        fontweight="bold",
        fontsize=24,
    )
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xticklabels([THEME_DISPLAY[theme] for theme in THEME_ORDER], rotation=35, ha="right")
    ax.set_yticklabels([THEME_DISPLAY[theme] for theme in THEME_ORDER], rotation=0)
    fig.tight_layout()
    fig.savefig(EXAMPLE_ROOT / "theme_interaction_heatmap.en.png", bbox_inches="tight")
    plt.close(fig)


def make_shortlist_heatmap() -> None:
    fig, ax = plt.subplots(figsize=(12, 6.8))
    sns.heatmap(
        SHORTLIST_MATRIX,
        cmap="YlGnBu",
        annot=True,
        fmt=".1f",
        linewidths=0.6,
        linecolor="white",
        vmin=2.5,
        vmax=5.0,
        cbar_kws={"label": "Author score (1-5)"},
        ax=ax,
    )
    ax.set_title(
        "Shortlist Evaluation Heatmap for LLM Training Directions",
        pad=16,
        fontweight="bold",
        fontsize=26,
    )
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.xticks(rotation=20, ha="right")
    plt.yticks(rotation=0)
    fig.tight_layout()
    fig.savefig(EXAMPLE_ROOT / "shortlist_heatmap.en.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    setup_style()
    _, idea_matrix = load_data()
    make_theme_interaction_heatmap(idea_matrix)
    make_shortlist_heatmap()


if __name__ == "__main__":
    main()
