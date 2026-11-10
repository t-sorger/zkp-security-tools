#!/usr/bin/env python3
"""Generate practitioner survey figures and tables.

Usage:
python3 scripts/generate_practitioner_artifacts.py \
--dev-csv responses/devs.csv \
--auditor-csv responses/auditors.csv \
--tool-categories-figure figures/practitioners_tool_categories.pdf \
--frameworks-figure figures/practitioners_frameworks.pdf \
--onboarding-figure figures/practitioners_tool_onboarding_effort.pdf \
--vulnerability-gaps-figure figures/practitioners_vulns_tool_gaps.pdf \
--missing-market-tools-figure figures/practitioners_missing_market_tools.pdf \
--overview-used-tools-figure figures/practitioners_overview_used_tools.pdf \
--overview-missing-tools-figure figures/practitioners_overview_missing_tools.pdf \
--overview-tool-traits-figure figures/practitioners_overview_tool_traits.pdf \
--tool-characteristics-figure figures/practitioners_tool_characteristics.pdf \
--tool-characteristics-table tables/practitioners_tool_characteristics.tex \
--vulnerability-perceptions-table tables/practitioners_vulnerability_perceptions.tex
"""

from __future__ import annotations

import csv
import argparse
import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


DEV: Path
AUD: Path
OUT_TOOL_CATEGORIES: Path
OUT_FRAMEWORKS: Path
OUT_ONBOARDING: Path
OUT_VULN_GAPS: Path
OUT_MISSING_MARKET_TOOLS: Path
OUT_OVERVIEW_USED_TOOLS: Path
OUT_OVERVIEW_MISSING_TOOLS: Path
OUT_OVERVIEW_TOOL_TRAITS: Path
OUT_TOOL_CHARACTERISTICS_FIGURE: Path
OUT_TOOL_CHARACTERISTICS_TABLE: Path
OUT_VULNERABILITY_PERCEPTIONS_TABLE: Path

DEV_TOOL_COL = (
    "Which of the following types of tools have you used for ZKP security "
    "analysis? Including potentially internal or paid tools. Select all that apply."
)
AUD_TOOL_COL = (
    "Which of the following types of tools have you used for ZKP security "
    "analysis? Including potentially internal tools. Select all that apply."
)
DEV_LANG_COL = (
    "For which languages or frameworks do you use security tools "
    "(excluding interactive LLMs)? Select all that apply."
)
AUD_LANG_COL = DEV_LANG_COL
DEV_ONBOARD_COL = (
    "How much effort is typically required to integrate security analysis or "
    "formal verification tools into your ZK codebase (e.g., specifications, "
    "frontends, CI)?"
)
AUD_ONBOARD_COL = (
    'How much effort is typically required to "onboard" a project into your '
    "advanced tooling/formal verification (e.g., writing frontends, custom "
    "specifications)? Skip the question if not applicable."
)
DEV_HARD_COL = "Which vulnerabilities do you think are more difficult to detect during development?"
AUD_HARD_COL = "Which vulnerabilities do you think are more difficult to detect manually? Select all that apply."
DEV_COVERED_COL = "Which vulnerabilities do you think are more adequately covered by security tools?"
AUD_COVERED_COL = "Which vulnerabilities do you think are more adequately covered by security tools? Select all that apply."
DEV_GAP_COL = (
    "Which vulnerabilities that you deem crucial cannot be detected by "
    "automated security tools (including LLMs) that you have used? Select all "
    "that apply."
)
AUD_GAP_COL = DEV_GAP_COL
DEV_MISSING_COL = "Which tools do you think are mostly missing on the market and would you use if available?"
AUD_MISSING_COL = (
    "Which tools do you think are mostly missing on the market and would you "
    "use if available? Select all that apply."
)

GROUP_COLORS = {"Developers": "#4C78A8", "Auditors": "#F58518"}
STACK_COLORS = {
    "Low": "#7AA874",
    "Moderate": "#E7BA52",
    "High": "#C44E52",
}


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def split_multi(value: str) -> list[str]:
    if not value or not value.strip():
        return []
    return [part.strip() for part in re.split(r"\s*;\s*", value.strip()) if part.strip()]


def answered_multi(data: list[dict[str, str]], col: str) -> list[list[str]]:
    return [split_multi(row.get(col, "")) for row in data if split_multi(row.get(col, ""))]


def answered_single(data: list[dict[str, str]], col: str) -> list[str]:
    return [row[col].strip() for row in data if row.get(col, "").strip()]


def pct(count: int, total: int) -> float:
    return 100 * count / total if total else 0.0


def selected_pct(data: list[dict[str, str]], col: str, predicates: list[str]) -> tuple[int, int, float]:
    answers = answered_multi(data, col)
    count = 0
    for answer in answers:
        if any(any(predicate.lower() in item.lower() for predicate in predicates) for item in answer):
            count += 1
    return count, len(answers), pct(count, len(answers))


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


def grouped_barh(
    out_path: Path,
    labels: list[str],
    dev_values: list[float],
    aud_values: list[float],
    *,
    width: float = 3.45,
    height: float = 2.75,
) -> None:
    y = np.arange(len(labels))
    bar_height = 0.34
    fig, ax = plt.subplots(figsize=(width, height))
    ax.barh(y - bar_height / 2, dev_values, height=bar_height, color=GROUP_COLORS["Developers"], label="Developers")
    ax.barh(y + bar_height / 2, aud_values, height=bar_height, color=GROUP_COLORS["Auditors"], label="Auditors")
    ax.set_xlim(0, 100)
    ax.set_xlabel("% of respondents")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, loc="lower right")
    fig.savefig(out_path)
    plt.close(fig)


def save_tool_categories(dev: list[dict[str, str]], aud: list[dict[str, str]]) -> None:
    specs = [
        ("Interactive LLMs", ["LLMs"]),
        ("Static analysis", ["Static analyser"]),
        ("Theorem provers/DSLs", ["Theorem Provers/DSLs"]),
        ("Fuzzers", ["Fuzzer for circuits"]),
        ("Formal verification", ["Formal Verification"]),
        ("Property/fuzz tests", ["Property-based"]),
        ("AI security tools", ["Automated tools leveraging AI"]),
    ]
    labels, dev_values, aud_values = [], [], []
    for label, needles in specs:
        labels.append(label)
        dev_values.append(selected_pct(dev, DEV_TOOL_COL, needles)[2])
        aud_values.append(selected_pct(aud, AUD_TOOL_COL, needles)[2])
    grouped_barh(OUT_TOOL_CATEGORIES, labels, dev_values, aud_values, height=2.75)


def save_frameworks(dev: list[dict[str, str]], aud: list[dict[str, str]]) -> None:
    specs = [
        ("Circom", ["Circom"]),
        ("Noir", ["Noir"]),
        ("Plonky3", ["Plonky3"]),
        ("zkVM guests", ["zkVM Guest"]),
        ("Halo2", ["Halo2"]),
        ("Gnark", ["Gnark"]),
        ("Cairo", ["Cairo"]),
        ("Leo", ["Leo"]),
    ]
    labels, dev_values, aud_values = [], [], []
    for label, needles in specs:
        labels.append(label)
        dev_values.append(selected_pct(dev, DEV_LANG_COL, needles)[2])
        aud_values.append(selected_pct(aud, AUD_LANG_COL, needles)[2])
    grouped_barh(OUT_FRAMEWORKS, labels, dev_values, aud_values, height=2.85)


def save_onboarding(dev: list[dict[str, str]], aud: list[dict[str, str]]) -> None:
    def counts(data: list[dict[str, str]], col: str) -> dict[str, float]:
        answers = answered_single(data, col)
        out = {"Low": 0, "Moderate": 0, "High": 0}
        for answer in answers:
            for key in out:
                if answer.startswith(key):
                    out[key] += 1
                    break
        return {key: pct(value, len(answers)) for key, value in out.items()}

    groups = ["Developers", "Auditors"]
    values = {"Developers": counts(dev, DEV_ONBOARD_COL), "Auditors": counts(aud, AUD_ONBOARD_COL)}
    y = np.arange(len(groups))
    left = np.zeros(len(groups))
    fig, ax = plt.subplots(figsize=(3.45, 1.35))
    for label in ["Low", "Moderate", "High"]:
        vals = [values[group][label] for group in groups]
        ax.barh(y, vals, left=left, color=STACK_COLORS[label], edgecolor="white", linewidth=0.5, label=label)
        for i, value in enumerate(vals):
            if value >= 10:
                ax.text(left[i] + value / 2, y[i], f"{value:.0f}", ha="center", va="center", fontsize=7)
        left += vals
    ax.set_xlim(0, 100)
    ax.set_xlabel("% of respondents")
    ax.set_yticks(y)
    ax.set_yticklabels(groups)
    ax.invert_yaxis()
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.28))
    fig.savefig(OUT_ONBOARDING)
    plt.close(fig)


VULN_MAP = [
    ("Underconstrained", ["Under-constrained circuits"]),
    ("Overconstrained", ["Over-constrained circuits"]),
    ("Range/arithmetic", ["Arithmetic field errors", "Bit decomposition"]),
    ("Public input/aliasing", ["Incorrect public input handling"]),
    ("Logic/semantic", ["Logic/semantic errors"]),
    ("Proof system", ["Unsound proof system"]),
    ("Fiat-Shamir", ["Fiat Shamir", "Fiat-Shamir"]),
    ("Crypto primitive", ["Hash function or cryptographic primitive misuse"]),
    ("System integration", ["Incorrect integration"]),
]


def save_gap_figure(dev: list[dict[str, str]], aud: list[dict[str, str]]) -> None:
    labels = ["Proof system", "Logic/semantic", "Crypto primitive", "Fiat-Shamir", "System integration", "Underconstrained"]
    lookup = dict(VULN_MAP)
    dev_values = [selected_pct(dev, DEV_GAP_COL, lookup[label])[2] for label in labels]
    aud_values = [selected_pct(aud, AUD_GAP_COL, lookup[label])[2] for label in labels]
    grouped_barh(OUT_VULN_GAPS, labels, dev_values, aud_values, height=2.35)


def save_missing_market(dev: list[dict[str, str]], aud: list[dict[str, str]]) -> None:
    specs = [
        ("Automated FV", ["Automated Formal Verification"]),
        ("LLM skills", ["LLM Skills"]),
        ("AI tools", ["AI Tools"]),
        ("Static analysis", ["Quick Static Analysis"]),
        ("General proof assistants", ["Proof Assistants", "Proof assistants"]),
        ("ZK-specific provers", ["Domain Specific Interactive Provers"]),
        ("Fuzzers", ["Fuzzers"]),
    ]
    labels, dev_values, aud_values = [], [], []
    for label, needles in specs:
        labels.append(label)
        dev_values.append(selected_pct(dev, DEV_MISSING_COL, needles)[2])
        aud_values.append(selected_pct(aud, AUD_MISSING_COL, needles)[2])
    grouped_barh(OUT_MISSING_MARKET_TOOLS, labels, dev_values, aud_values, height=2.65)


TOOL_CATEGORY_SPECS = [
    ("Interactive\nLLMs", ["LLMs"]),
    ("Static\nanalysis", ["Static analyser"]),
    ("Theorem\nprovers", ["Theorem Provers/DSLs"]),
    ("Fuzzers", ["Fuzzer for circuits"]),
    ("Formal\nverification", ["Formal Verification"]),
    ("Property-based\ntesting", ["Property-based"]),
    ("AI security\ntools", ["Automated tools leveraging AI"]),
]

GAP_SPECS = [
    ("Proof-system\nissues", ["Unsound proof system"]),
    ("Logic/semantic\nerrors", ["Logic/semantic errors"]),
    ("Crypto\nmisuse", ["Hash function or cryptographic primitive misuse"]),
    ("Fiat-Shamir", ["Fiat Shamir", "Fiat-Shamir"]),
    ("System\nintegration", ["Incorrect integration"]),
    ("Underconstrained\ncircuits", ["Under-constrained circuits"]),
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


def grouped_bars(
    ax,
    data: list[dict[str, str]],
    other: list[dict[str, str]],
    data_col: str,
    other_col: str,
    specs: list[tuple[str, list[str]]],
    title: str,
) -> None:
    labels = [label for label, _ in specs]
    dev_values = [selected_pct(data, data_col, needles)[2] for _, needles in specs]
    aud_values = [selected_pct(other, other_col, needles)[2] for _, needles in specs]
    plot_grouped_bars(ax, labels, dev_values, aud_values, title)


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


def save_survey_overview_panels(dev: list[dict[str, str]], aud: list[dict[str, str]]) -> None:
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


def save_survey_overview(dev: list[dict[str, str]], aud: list[dict[str, str]], out_path: Path) -> None:
    fig, axes = plt.subplots(1, 4, figsize=(7.15, 2.45), sharex=True)
    grouped_bars(axes[0], dev, aud, DEV_TOOL_COL, AUD_TOOL_COL, TOOL_CATEGORY_SPECS, "(a) Used tools")
    grouped_bars(axes[1], dev, aud, DEV_GAP_COL, AUD_GAP_COL, GAP_SPECS, "(b) Unsupported bugs")
    grouped_bars(axes[2], dev, aud, DEV_MISSING_COL, AUD_MISSING_COL, MISSING_TOOL_SPECS, "(c) Missing tools")
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
    plot_grouped_bars(
        axes[3],
        [characteristic_labels[label] for label, _, _ in characteristic_rows],
        [dev_value for _, dev_value, _ in characteristic_rows],
        [aud_value for _, _, aud_value in characteristic_rows],
        "(d) Tool traits",
    )
    for ax in axes:
        ax.set_xlabel("%", fontsize=5.8)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 1.02), fontsize=6.4)
    fig.tight_layout(w_pad=0.45, rect=(0, 0, 1, 0.93))
    fig.savefig(out_path)
    plt.close(fig)


def latex_escape(text: str) -> str:
    return (
        text.replace("&", r"\&")
        .replace("%", r"\%")
        .replace("_", r"\_")
        .replace("#", r"\#")
    )


def cell(count: int, total: int) -> str:
    return rf"{count}/{total} ({pct(count, total):.0f}\%)"


def characteristic_values(dev: list[dict[str, str]], aud: list[dict[str, str]]) -> list[tuple[str, float, float]]:
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

    def agree_counts(data: list[dict[str, str]], label_fragment: str) -> tuple[int, int]:
        col = next(col for col in data[0] if "Below we enumerate" in col and label_fragment in col)
        answers = answered_single(data, col)
        count = sum(1 for answer in answers if answer in {"Agree", "Strongly Agree"})
        return count, len(answers)

    for fragment, label in labels.items():
        dev_count, dev_total = agree_counts(dev, fragment)
        aud_count, aud_total = agree_counts(aud, fragment)
        rows_out.append((label, pct(dev_count, dev_total), pct(aud_count, aud_total)))
    return rows_out


def save_characteristics_figure(dev: list[dict[str, str]], aud: list[dict[str, str]]) -> None:
    values = characteristic_values(dev, aud)
    labels = [label for label, _, _ in values]
    y = np.arange(len(labels))
    bar_height = 0.34
    fig, ax = plt.subplots(figsize=(3.45, 2.55))
    dev_values = [dev_value for _, dev_value, _ in values]
    aud_values = [aud_value for _, _, aud_value in values]
    ax.barh(y - bar_height / 2, dev_values, height=bar_height, color=GROUP_COLORS["Developers"], label="Developers")
    ax.barh(y + bar_height / 2, aud_values, height=bar_height, color=GROUP_COLORS["Auditors"], label="Auditors")
    for index, value in enumerate(dev_values):
        ax.text(value + 1.2, y[index] - bar_height / 2, f"{value:.0f}", va="center", fontsize=6.2)
    for index, value in enumerate(aud_values):
        ax.text(value + 1.2, y[index] + bar_height / 2, f"{value:.0f}", va="center", fontsize=6.2)
    ax.set_xlim(0, 100)
    ax.set_xlabel("% Agree or Strongly Agree")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.12))
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(OUT_TOOL_CHARACTERISTICS_FIGURE)
    plt.close(fig)


def write_characteristics_table(dev: list[dict[str, str]], aud: list[dict[str, str]]) -> None:
    rows_out = []
    for label, dev_value, aud_value in characteristic_values(dev, aud):
        rows_out.append((label, rf"{dev_value:.0f}\%", rf"{aud_value:.0f}\%"))
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Tool characteristics rated important by practitioners. Cells report Agree or Strongly Agree over respondents who answered each item.}",
        r"\label{tab:practitioner-tool-characteristics}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{3pt}",
        r"\begin{tabular}{@{}p{0.50\columnwidth}cc@{}}",
        r"\toprule",
        r"\textbf{Characteristic} & \textbf{Dev.} & \textbf{Aud.} \\",
        r"\midrule",
    ]
    lines += [rf"{latex_escape(label)} & {dev_cell} & {aud_cell} \\" for label, dev_cell, aud_cell in rows_out]
    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
    ]
    OUT_TOOL_CHARACTERISTICS_TABLE.write_text("\n".join(lines) + "\n")


def count_vuln(data: list[dict[str, str]], col: str, needles: list[str]) -> tuple[int, int]:
    return selected_pct(data, col, needles)[:2]


def write_vulnerability_table(dev: list[dict[str, str]], aud: list[dict[str, str]]) -> None:
    display_labels = {
        "Underconstrained": "Underconstrained circuits",
        "Overconstrained": "Overconstrained circuits",
        "Range/arithmetic": "Arithmetic issues",
        "Public input/aliasing": "Public input/aliasing",
        "Logic/semantic": "Semantic mismatches",
        "Proof system": "Proof-system issues",
        "Fiat-Shamir": "Fiat-Shamir",
        "Crypto primitive": "Crypto primitive misuse",
        "System integration": "System integration",
    }

    def pct_cell(count: int, total: int) -> str:
        value = pct(count, total)
        if value == 0:
            return r"0\%"
        shade = min(28, max(7, round(value * 0.34)))
        return rf"\cellcolor{{cyan!{shade}}}{value:.0f}\%"

    lines = [
        r"\centering",
        r"\captionof{table}{Practitioners' views of vulnerabilities and tools (including LLMs). Hard: hard to detect manually. Covered: adequately covered by tools.}",
        r"\label{tab:practitioner-vulnerability-perceptions}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{3pt}",
        r"\renewcommand{\arraystretch}{1.08}",
        r"\begin{tabular}{@{}p{0.52\linewidth}cc@{}}",
        r"\toprule",
        r"\textbf{Class} & \textbf{Hard} & \textbf{Covered} \\",
        r"\midrule",
    ]
    for label, needles in VULN_MAP:
        if label in {"Overconstrained", "Public input/aliasing"}:  # not reported in the paper's table
            continue
        dh, dhn = count_vuln(dev, DEV_HARD_COL, needles)
        dc, dcn = count_vuln(dev, DEV_COVERED_COL, needles)
        ah, ahn = count_vuln(aud, AUD_HARD_COL, needles)
        ac, acn = count_vuln(aud, AUD_COVERED_COL, needles)
        lines.append(
            rf"{latex_escape(display_labels[label])} & "
            rf"{pct_cell(dh + ah, dhn + ahn)} & "
            rf"{pct_cell(dc + ac, dcn + acn)} \\"
        )
    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"\renewcommand{\arraystretch}{1.0}",
    ]
    OUT_VULNERABILITY_PERCEPTIONS_TABLE.write_text("\n".join(lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dev-csv", required=True, type=Path)
    parser.add_argument("--auditor-csv", required=True, type=Path)
    parser.add_argument("--tool-categories-figure", required=True, type=Path)
    parser.add_argument("--frameworks-figure", required=True, type=Path)
    parser.add_argument("--onboarding-figure", required=True, type=Path)
    parser.add_argument("--vulnerability-gaps-figure", required=True, type=Path)
    parser.add_argument("--missing-market-tools-figure", required=True, type=Path)
    parser.add_argument("--overview-used-tools-figure", required=True, type=Path)
    parser.add_argument("--overview-missing-tools-figure", required=True, type=Path)
    parser.add_argument("--overview-tool-traits-figure", required=True, type=Path)
    parser.add_argument("--tool-characteristics-figure", required=True, type=Path)
    parser.add_argument("--tool-characteristics-table", required=True, type=Path)
    parser.add_argument("--vulnerability-perceptions-table", required=True, type=Path)
    return parser.parse_args()


def ensure_output_parents(paths: list[Path]) -> None:
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)


def main() -> None:
    global DEV, AUD
    global OUT_TOOL_CATEGORIES, OUT_FRAMEWORKS, OUT_ONBOARDING
    global OUT_VULN_GAPS, OUT_MISSING_MARKET_TOOLS
    global OUT_OVERVIEW_USED_TOOLS, OUT_OVERVIEW_MISSING_TOOLS, OUT_OVERVIEW_TOOL_TRAITS
    global OUT_TOOL_CHARACTERISTICS_FIGURE, OUT_TOOL_CHARACTERISTICS_TABLE
    global OUT_VULNERABILITY_PERCEPTIONS_TABLE

    args = parse_args()
    DEV = args.dev_csv
    AUD = args.auditor_csv
    OUT_TOOL_CATEGORIES = args.tool_categories_figure
    OUT_FRAMEWORKS = args.frameworks_figure
    OUT_ONBOARDING = args.onboarding_figure
    OUT_VULN_GAPS = args.vulnerability_gaps_figure
    OUT_MISSING_MARKET_TOOLS = args.missing_market_tools_figure
    OUT_OVERVIEW_USED_TOOLS = args.overview_used_tools_figure
    OUT_OVERVIEW_MISSING_TOOLS = args.overview_missing_tools_figure
    OUT_OVERVIEW_TOOL_TRAITS = args.overview_tool_traits_figure
    OUT_TOOL_CHARACTERISTICS_FIGURE = args.tool_characteristics_figure
    OUT_TOOL_CHARACTERISTICS_TABLE = args.tool_characteristics_table
    OUT_VULNERABILITY_PERCEPTIONS_TABLE = args.vulnerability_perceptions_table

    ensure_output_parents(
        [
            OUT_TOOL_CATEGORIES,
            OUT_FRAMEWORKS,
            OUT_ONBOARDING,
            OUT_VULN_GAPS,
            OUT_MISSING_MARKET_TOOLS,
            OUT_OVERVIEW_USED_TOOLS,
            OUT_OVERVIEW_MISSING_TOOLS,
            OUT_OVERVIEW_TOOL_TRAITS,
            OUT_TOOL_CHARACTERISTICS_FIGURE,
            OUT_TOOL_CHARACTERISTICS_TABLE,
            OUT_VULNERABILITY_PERCEPTIONS_TABLE,
        ]
    )
    setup_style()
    dev = rows(DEV)
    aud = rows(AUD)
    save_tool_categories(dev, aud)
    save_frameworks(dev, aud)
    save_onboarding(dev, aud)
    save_gap_figure(dev, aud)
    save_missing_market(dev, aud)
    save_survey_overview_panels(dev, aud)
    save_characteristics_figure(dev, aud)
    write_characteristics_table(dev, aud)
    write_vulnerability_table(dev, aud)


if __name__ == "__main__":
    main()
