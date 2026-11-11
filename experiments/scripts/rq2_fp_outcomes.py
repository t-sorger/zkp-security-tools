#!/usr/bin/env python3
"""Generate Figure 3 (false-positive experiment outcomes) from the zkHydra FP results.

Usage (from experiments/):
    python3 scripts/rq2_fp_outcomes.py \
        --fp-results-dir results/fp \
        --fp-outcomes-figure figures/rq2_fp_outcomes.pdf

Reads:
    <fp_results_dir>/<circuit>/fp_candidates.json      per tool: run status and soundness alerts
    <fp_results_dir>/<circuit>/<tool>/fp_triage.json   the authors' verdict for each soundness alert
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

from rq2_tool_outcomes import OUTCOME_COLORS, setup_style

# Same order and names as the tool-outcomes figure.
TOOLS = {
    "picus": "Picus",
    "circom_civer": "Civer",
    "circomspect": "Circomspect",
    "zkfuzz": "zkFuzz",
    "conscs": "ConsCS",
}
# Per tool and circuit: "FP" = >=1 false-positive alert, "No FP" = no alert or only real issues.
OUTCOMES = {
    "No FP": OUTCOME_COLORS["FN"],
    "FP": "#DD8452",
    "Error": OUTCOME_COLORS["Error"],
    "Timeout": OUTCOME_COLORS["Timeout"],
}


def load_counts(results_dir: Path) -> tuple[dict[str, Counter], int]:
    """Per tool: how many circuits end in each outcome."""
    counts = {tool: Counter() for tool in TOOLS}
    circuits = sorted(results_dir.glob("*/fp_candidates.json"))
    for cand_path in circuits:
        cand = json.loads(cand_path.read_text())
        for tool, c in counts.items():
            entry = cand["tools"][tool]
            if entry["status"] == "timeout":
                c["Timeout"] += 1
                continue
            if entry["status"] != "success":
                c["Error"] += 1
                continue
            triage = cand_path.parent / tool / "fp_triage.json"
            verdicts = Counter(r["status"] for r in json.loads(triage.read_text())) if triage.is_file() else Counter()
            assert sum(verdicts.values()) == entry["soundness_count"], f"unreviewed alerts in {triage}"
            c["FP" if verdicts["FalsePositive"] else "No FP"] += 1
    return counts, len(circuits)


def save_fp_outcomes(counts: dict[str, Counter], n_circuits: int, out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(3.45, 1.75))
    y = np.arange(len(TOOLS))
    left = np.zeros(len(TOOLS))
    for outcome, color in OUTCOMES.items():
        values = np.array([counts[tool][outcome] for tool in TOOLS])
        ax.barh(y, values, left=left, color=color, edgecolor="white", linewidth=0.5, label=outcome)
        for row, value in enumerate(values):
            if value:
                text_color = "#222222" if outcome == "No FP" else "white"
                ax.text(left[row] + value / 2, y[row], str(int(value)),
                        ha="center", va="center", fontsize=5.8, color=text_color)
        left += values

    ax.set_xlim(0, n_circuits)
    ax.set_yticks(y)
    ax.set_yticklabels(list(TOOLS.values()), fontsize=6.4)
    ax.invert_yaxis()
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.tick_params(axis="x", labelsize=6.1)
    ax.set_axisbelow(True)
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlabel("Total Circuits", fontsize=6.6)

    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=len(OUTCOMES), frameon=False, fontsize=6.6)
    fig.savefig(out_path)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fp-results-dir", required=True, type=Path)
    parser.add_argument("--fp-outcomes-figure", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.fp_outcomes_figure.parent.mkdir(parents=True, exist_ok=True)
    counts, n_circuits = load_counts(args.fp_results_dir)
    setup_style()
    save_fp_outcomes(counts, n_circuits, args.fp_outcomes_figure)


if __name__ == "__main__":
    main()
