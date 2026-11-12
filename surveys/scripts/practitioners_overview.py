#!/usr/bin/env python3
"""Generate Figure 5 (practitioner survey overview: used tools, tool traits, missing tools) from the aggregated survey responses.

Usage (from surveys/):
python3 scripts/practitioners_overview.py \
--dev-csv responses/devs_aggregated.csv \
--auditor-csv responses/auditors_aggregated.csv \
--overview-used-tools-figure figures/practitioners_overview_used_tools.pdf \
--overview-missing-tools-figure figures/practitioners_overview_missing_tools.pdf \
--overview-tool-traits-figure figures/practitioners_overview_tool_traits.pdf
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

DEV: Path
AUD: Path
OUT_OVERVIEW_USED_TOOLS: Path
OUT_OVERVIEW_MISSING_TOOLS: Path
OUT_OVERVIEW_TOOL_TRAITS: Path

DEV_TOOL_COL = (
    "Which of the following types of tools have you used for ZKP security "
    "analysis? Including potentially internal or paid tools. Select all that apply."
)
AUD_TOOL_COL = (
    "Which of the following types of tools have you used for ZKP security "
    "analysis? Including potentially internal tools. Select all that apply."
)
DEV_MISSING_COL = "Which tools do you think are mostly missing on the market and would you use if available?"
AUD_MISSING_COL = (
    "Which tools do you think are mostly missing on the market and would you "
    "use if available? Select all that apply."
)

GROUP_COLORS = {"Developers": "#4C78A8", "Auditors": "#F58518"}

# question -> (respondents who answered it, {answer: respondents who chose it})
Counts = dict[str, tuple[int, dict[str, int]]]


def load_aggregated(path: Path) -> Counts:
    data: Counts = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            _, answers = data.setdefault(row["question"], (int(row["answered"]), {}))
            answers[row["answer"]] = int(row["count"])
    return data


def pct(count: int, total: int) -> float:
    return 100 * count / total if total else 0.0


def selected_pct(data: Counts, col: str, predicates: list[str]) -> tuple[int, int, float]:
    answered, answers = data[col]
    matches = [n for answer, n in answers.items() if any(p.lower() in answer.lower() for p in predicates)]
    # Summing two answers would count respondents who chose both twice.
    assert len(matches) <= 1, f"{predicates} match {len(matches)} answers of {col!r}"
    count = sum(matches)
    return count, answered, pct(count, answered)


def setup_style() -> None:
    # Plain matplotlib style, as used for the paper's survey figures (no seaborn).
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


TOOL_CATEGORY_SPECS = [
    ("Interactive\nLLMs", ["LLMs"]),
    ("Static\nanalysis", ["Static analyser"]),
    ("Theorem\nprovers", ["Theorem Provers/DSLs"]),
    ("Fuzzers", ["Fuzzer for circuits"]),
    ("Formal\nverification", ["Formal Verification"]),
    ("Property-based\ntesting", ["Property-based"]),
    ("AI security\ntools", ["Automated tools leveraging AI"]),
]


MISSING_TOOL_SPECS = [
    ("Automated\nFV", ["Automated Formal Verification"]),
    ("Reusable\nLLM skills", ["LLM Skills"]),
    ("AI security\ntools", ["AI Tools"]),
    ("Static\nanalysis", ["Quick Static Analysis"]),
    ("General proof\nassistants", ["Proof Assistants", "Proof assistants"]),
    ("ZK-specific\nprovers", ["Domain Specific Interactive Provers"]),
    ("Fuzzers", ["Fuzzers"]),
]


def plot_grouped_bars(
    ax,
    labels: list[str],
    dev_values: list[float],
    aud_values: list[float],
    title: str | None = None,
) -> None:
    y = np.arange(len(labels)) * 0.86
    height = 0.36
    ax.barh(y - height / 2, dev_values, height, color=GROUP_COLORS["Developers"], label="Developers")
    ax.barh(y + height / 2, aud_values, height, color=GROUP_COLORS["Auditors"], label="Auditors")
    if title:
        ax.set_title(title, fontsize=7.4, pad=2)
    ax.set_xlim(0, 100)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7.2, linespacing=0.94)
    ax.set_ylim(y[-1] + 0.5, -0.5)
    ax.tick_params(axis="x", labelsize=5.8)
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_overview_panel(
    out_path: Path,
    labels: list[str],
    dev_values: list[float],
    aud_values: list[float],
    *,
    height: float = 2.35,
) -> None:
    fig, ax = plt.subplots(figsize=(1.88, height))
    plot_grouped_bars(ax, labels, dev_values, aud_values)
    ax.set_xlabel("%", fontsize=6.1)
    fig.tight_layout(pad=0.1)
    fig.savefig(out_path)
    plt.close(fig)


def save_survey_overview_panels(dev: Counts, aud: Counts) -> None:
    labels = [label for label, _ in TOOL_CATEGORY_SPECS]
    save_overview_panel(
        OUT_OVERVIEW_USED_TOOLS,
        labels,
        [selected_pct(dev, DEV_TOOL_COL, needles)[2] for _, needles in TOOL_CATEGORY_SPECS],
        [selected_pct(aud, AUD_TOOL_COL, needles)[2] for _, needles in TOOL_CATEGORY_SPECS],
    )

    labels = [label for label, _ in MISSING_TOOL_SPECS]
    save_overview_panel(
        OUT_OVERVIEW_MISSING_TOOLS,
        labels,
        [selected_pct(dev, DEV_MISSING_COL, needles)[2] for _, needles in MISSING_TOOL_SPECS],
        [selected_pct(aud, AUD_MISSING_COL, needles)[2] for _, needles in MISSING_TOOL_SPECS],
    )

    characteristic_labels = {
        "Low false positives": "Low false\npositives",
        "Ease of use": "Ease",
        "Documentation": "Docs",
        "Report quality": "Report\nquality",
        "Scalability": "Scale",
        "PoC generation": "PoC\ngeneration",
        "Cost": "Cost",
        "CI/CD integration": "CI/CD\nintegration",
        "Completeness confidence": "Completeness\nconfidence",
    }
    characteristic_rows = characteristic_values(dev, aud)
    save_overview_panel(
        OUT_OVERVIEW_TOOL_TRAITS,
        [characteristic_labels[label] for label, _, _ in characteristic_rows],
        [dev_value for _, dev_value, _ in characteristic_rows],
        [aud_value for _, _, aud_value in characteristic_rows],
        height=2.55,
    )


def characteristic_values(dev: Counts, aud: Counts) -> list[tuple[str, float, float]]:
    rows_out = []
    labels = {
        "Low false positives": "Low false positives",
        "Ease of use": "Ease of use",
        "Documentation": "Documentation",
        "Report quality": "Report quality",
        "Scalability/performance": "Scalability",
        "Producing PoC": "PoC generation",
        "Cost": "Cost",
        "Integration with CI/CD": "CI/CD integration",
        "Confidence of completeness": "Completeness confidence",
    }

    def agree_counts(data: Counts, label_fragment: str) -> tuple[int, int]:
        col = next(col for col in data if "Below we enumerate" in col and label_fragment in col)
        answered, answers = data[col]
        return answers.get("Agree", 0) + answers.get("Strongly Agree", 0), answered

    for fragment, label in labels.items():
        dev_count, dev_total = agree_counts(dev, fragment)
        aud_count, aud_total = agree_counts(aud, fragment)
        rows_out.append((label, pct(dev_count, dev_total), pct(aud_count, aud_total)))
    return rows_out


def ensure_output_parents(paths: list[Path]) -> None:
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dev-csv", required=True, type=Path)
    parser.add_argument("--auditor-csv", required=True, type=Path)
    parser.add_argument("--overview-used-tools-figure", required=True, type=Path)
    parser.add_argument("--overview-missing-tools-figure", required=True, type=Path)
    parser.add_argument("--overview-tool-traits-figure", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    global DEV, AUD
    global OUT_OVERVIEW_USED_TOOLS, OUT_OVERVIEW_MISSING_TOOLS, OUT_OVERVIEW_TOOL_TRAITS

    args = parse_args()
    DEV = args.dev_csv
    AUD = args.auditor_csv
    OUT_OVERVIEW_USED_TOOLS = args.overview_used_tools_figure
    OUT_OVERVIEW_MISSING_TOOLS = args.overview_missing_tools_figure
    OUT_OVERVIEW_TOOL_TRAITS = args.overview_tool_traits_figure

    ensure_output_parents([OUT_OVERVIEW_USED_TOOLS, OUT_OVERVIEW_MISSING_TOOLS, OUT_OVERVIEW_TOOL_TRAITS])
    setup_style()
    save_survey_overview_panels(load_aggregated(DEV), load_aggregated(AUD))


if __name__ == "__main__":
    main()
