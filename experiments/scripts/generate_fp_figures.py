#!/usr/bin/env python3
"""Generate the false-positive experiment figure and table from the zkHydra FP results.

Usage (from experiments/):
    python3 scripts/generate_fp_figures.py \
        --fp-results-dir results/fp \
        --fp-outcomes-figure figures/rq2_fp_outcomes.pdf \
        --fp-table tables/rq2_fp_results.tex

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
from generate_rq2_figures import OUTCOME_COLORS, setup_style
from matplotlib.ticker import MultipleLocator

# Same order and names as the tool-outcomes figure; LaTeX macros as used in the paper.
TOOLS = {
    "picus": ("Picus", r"\picus"),
    "circom_civer": ("Civer", r"\civer"),
    "circomspect": ("Circomspect", r"\circomspect"),
    "zkfuzz": ("zkFuzz", r"\zkfuzz"),
    "conscs": ("ConsCS", r"\conscs"),
}
# Per tool and circuit: "FP" = >=1 false-positive alert, "No FP" = no alert or only real issues.
OUTCOMES = {
    "No FP": OUTCOME_COLORS["FN"],
    "FP": "#DD8452",
    "Error": OUTCOME_COLORS["Error"],
    "Timeout": OUTCOME_COLORS["Timeout"],
}


def load_counts(results_dir: Path) -> tuple[dict[str, Counter], int, int]:
    """Per tool: run outcomes and verdict counts on completed runs."""
    counts = {tool: Counter() for tool in TOOLS}
    circuits = sorted(results_dir.glob("*/fp_candidates.json"))
    projects = set()
    for cand_path in circuits:
        cand = json.loads(cand_path.read_text())
        projects.add(cand["provenance"]["ProjectName"])
        for tool, c in counts.items():
            entry = cand["tools"][tool]
            if entry["status"] == "timeout":
                c["Timeout"] += 1
                continue
            if entry["status"] != "success":
                c["Error"] += 1
                continue
            c["Done"] += 1
            c["Alerts"] += entry["soundness_count"]
            triage = cand_path.parent / tool / "fp_triage.json"
            verdicts = Counter(r["status"] for r in json.loads(triage.read_text())) if triage.is_file() else Counter()
            assert sum(verdicts.values()) == entry["soundness_count"], f"unreviewed alerts in {triage}"
            c.update(verdicts)
            c["FP" if verdicts["FalsePositive"] else "No FP"] += 1
    return counts, len(circuits), len(projects)


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
    ax.set_yticklabels([name for name, _ in TOOLS.values()], fontsize=6.4)
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


def write_fp_table(counts: dict[str, Counter], n_circuits: int, n_projects: int, out_path: Path) -> None:
    def row(name: str, c: Counter, fp_circ: str) -> str:
        cells = [c[k] for k in ("Done", "Timeout", "Error", "Alerts", "FalsePositive", "RealIssue")]
        return " & ".join([name, *map(str, cells), fp_circ]) + r" \\"

    total = sum(counts.values(), Counter())
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{",
        rf"    False-positive experiment on {n_circuits} circuits from {n_projects} audited projects.",
        r"    Done, Timeout (TO), and Error (Err) count runs that completed, timed out, or failed.",
        r"    Alerts are soundness alerts, triaged into false positives (FP) and real issues (Real).",
        r"    FP circ.\ counts circuits with at least one FP among completed runs.",
        r"}",
        r"\label{tab:rq2-fp}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{4pt}",
        r"\begin{tabular}{lrrrrrrr}",
        r"\toprule",
        r"\textbf{Tool} & Done & TO & Err & Alerts & FP & Real & FP circ. \\",
        r"\midrule",
        *(row(TOOLS[t][1], counts[t], f"{counts[t]['FP']}/{counts[t]['Done']}") for t in TOOLS),
        r"\midrule",
        row(r"\textbf{Total}", total, "--"),
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
        "",
    ]
    out_path.write_text("\n".join(lines))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fp-results-dir", required=True, type=Path)
    parser.add_argument("--fp-outcomes-figure", required=True, type=Path)
    parser.add_argument("--fp-table", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.fp_outcomes_figure.parent.mkdir(parents=True, exist_ok=True)
    args.fp_table.parent.mkdir(parents=True, exist_ok=True)
    counts, n_circuits, n_projects = load_counts(args.fp_results_dir)
    setup_style()
    save_fp_outcomes(counts, n_circuits, args.fp_outcomes_figure)
    write_fp_table(counts, n_circuits, n_projects, args.fp_table)


if __name__ == "__main__":
    main()
