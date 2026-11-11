#!/usr/bin/env python3
"""Generate Figure 2 (per-tool outcomes in isolated and project mode) from the tool-evaluation summary.

Usage (from experiments/):
    python3 scripts/rq2_tool_outcomes.py \
        --tools-evaluation-json data/tools-evaluation.json \
        --tool-outcomes-figure figures/rq2_tool_outcomes.pdf
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUTCOMES = ["TP", "FN", "Error", "Timeout"]
OUTCOME_COLORS = {
    "TP": "#2F7D4A",
    "FN": "#C9CDD3",
    "Error": "#C44E52",
    "Timeout": "#5B6EA6",
}
MODE_LABELS = {
    "direct": "Isolated mode",
    "original": "Project mode",
}


def load_data(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def setup_style() -> None:
    try:
        import seaborn as sns  # type: ignore

        sns.set_theme(
            context="paper",
            style="whitegrid",
            font_scale=0.86,
            rc={
                "axes.edgecolor": "#333333",
                "axes.linewidth": 0.6,
                "grid.color": "#E2E4E8",
                "grid.linewidth": 0.5,
                "font.family": "serif",
            },
        )
    except ImportError:
        plt.rcParams.update(
            {
                "axes.edgecolor": "#333333",
                "axes.linewidth": 0.6,
                "axes.grid": True,
                "grid.color": "#E2E4E8",
                "grid.linewidth": 0.5,
                "font.family": "serif",
                "font.size": 8,
                "legend.fontsize": 7,
                "axes.titlesize": 8.5,
                "axes.labelsize": 8,
                "xtick.labelsize": 7,
                "ytick.labelsize": 7,
            }
        )

    plt.rcParams.update(
        {
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "figure.dpi": 200,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.02,
        }
    )


def classify_run(result: dict) -> str:
    verdict = result.get("verdict")
    match = result.get("details", {}).get("ground_truth_match")
    if verdict == "vulnerable" and match == "TruePositive":
        return "TP"
    if verdict == "error":
        return "Error"
    if verdict == "timeout":
        return "Timeout"
    return "FN"


def tool_outcomes(data: dict, mode: str) -> dict[str, Counter]:
    counts = {tool["id"]: Counter() for tool in data["tools"]}
    for bug in data["modes"][mode]["bugs"]:
        for tool_id, result in bug["tools"].items():
            counts[tool_id][classify_run(result)] += 1
    return counts


def detected_by_any_tool(bug: dict) -> bool:
    return any(classify_run(result) == "TP" for result in bug["tools"].values())


def cumulative_outcome(data: dict, mode: str) -> Counter:
    bugs = data["modes"][mode]["bugs"]
    detected = sum(detected_by_any_tool(bug) for bug in bugs)
    return Counter({"TP": detected, "FN": len(bugs) - detected})


def save_tool_outcomes(data: dict, out_path: Path) -> None:
    tools = data["tools"]
    tool_ids = [tool["id"] for tool in tools] + ["all"]
    tool_names = [tool["name"] for tool in tools] + ["All tools"]

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(3.45, 3.35),
        gridspec_kw={"hspace": 0.42},
    )

    for index, (ax, mode) in enumerate(zip(axes, ["direct", "original"])):
        counts = tool_outcomes(data, mode)
        counts["all"] = cumulative_outcome(data, mode)
        y = np.arange(len(tool_ids))
        left = np.zeros(len(tool_ids))

        for outcome in OUTCOMES:
            values = np.array([counts[tool_id][outcome] for tool_id in tool_ids])
            ax.barh(
                y,
                values,
                left=left,
                color=OUTCOME_COLORS[outcome],
                edgecolor="white",
                linewidth=0.5,
                label=outcome,
            )
            for row_index, value in enumerate(values):
                if value >= 4:
                    color = "white" if outcome in {"TP", "Error", "Timeout"} else "#222222"
                    ax.text(
                        left[row_index] + value / 2,
                        y[row_index],
                        str(int(value)),
                        ha="center",
                        va="center",
                        fontsize=5.8,
                        color=color,
                    )
            left += values

        ax.set_title(f"{MODE_LABELS[mode]} (n={data['modes'][mode]['total_bugs']})")
        ax.set_xlim(0, data["modes"][mode]["total_bugs"])
        ax.set_yticks(y)
        ax.set_yticklabels(tool_names, fontsize=6.4)
        ax.axhline(len(tool_ids) - 1.5, color="#6B7280", linewidth=0.5)
        ax.invert_yaxis()
        ax.tick_params(axis="x", labelsize=6.1)
        ax.set_axisbelow(True)
        ax.grid(axis="x")
        ax.grid(axis="y", visible=False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        if index == 0:
            ax.set_xlabel("")
        else:
            ax.set_xlabel("Total Bugs", fontsize=6.6)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=len(OUTCOMES),
        frameon=False,
        bbox_to_anchor=(0.5, 1.01),
        fontsize=6.6,
    )
    fig.subplots_adjust(left=0.23, right=0.99, bottom=0.10, top=0.90, hspace=0.42)
    fig.savefig(out_path)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tools-evaluation-json", required=True, type=Path)
    parser.add_argument("--tool-outcomes-figure", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.tool_outcomes_figure.parent.mkdir(parents=True, exist_ok=True)
    setup_style()
    save_tool_outcomes(load_data(args.tools_evaluation_json), args.tool_outcomes_figure)


if __name__ == "__main__":
    main()
