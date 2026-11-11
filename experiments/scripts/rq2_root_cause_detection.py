#!/usr/bin/env python3
"""Generate Table 4 (cumulative detection by ground-truth root cause) from the tool-evaluation summary.

Usage (from experiments/):
    python3 scripts/rq2_root_cause_detection.py \
        --tools-evaluation-json data/tools-evaluation.json \
        --root-cause-table tables/rq2_root_cause_detection.tex
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from rq2_tool_outcomes import detected_by_any_tool, load_data

ROOT_CAUSE_LABELS = {
    "Missing Input Constraints": "Missing input constraints",
    "Wrong Translation of Logic into Constraints": "Logic-to-constraint translation",
    "Unsafe Reuse of Circuit": "Unsafe circuit reuse",
    "Assigned but Unconstrained": "Assigned but unconstrained",
    "Circuit Design Issue": "Circuit design issue",
    "Arithmetic Field Issues": "Arithmetic field issues",
    "Misimplementation of a Specification": "Spec. misimplementation",
    "Other Programming Errors": "Other programming errors",
}


def root_cause_detection(data: dict, mode: str) -> dict[str, tuple[int, int]]:
    counts: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for bug in data["modes"][mode]["bugs"]:
        root_cause = bug["ground_truth"]["root_cause"]
        counts[root_cause][0] += 1
        counts[root_cause][1] += int(detected_by_any_tool(bug))
    return {key: (total, detected) for key, (total, detected) in counts.items()}


def latex_escape(text: str) -> str:
    return text.replace("&", r"\&")


def write_root_cause_table(data: dict, out_path: Path) -> None:
    direct = root_cause_detection(data, "direct")
    original = root_cause_detection(data, "original")
    order = sorted(direct.keys(), key=lambda key: (-direct[key][0], key))

    def detected_cell(detected: int, total: int) -> str:
        return rf"{detected}/{total} ({100 * detected / total:.1f}\%)"

    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Cumulative detection by ground-truth root cause.}",
        r"\label{tab:rq2-root-cause-detection}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{3pt}",
        r"\begin{tabular}{@{}p{0.50\columnwidth}cc@{}}",
        r"\toprule",
        r"\textbf{Root cause} &",
        r"\textbf{Isolated} &",
        r"\textbf{Project} \\",
        r"\midrule",
    ]

    for index, root_cause in enumerate(order):
        d_total, d_detected = direct[root_cause]
        o_total, o_detected = original[root_cause]
        label = ROOT_CAUSE_LABELS.get(root_cause, root_cause)
        row_prefix = r"\rowcolor{gainsboro}" if index % 2 == 0 else ""
        lines.append(
            f"{row_prefix}{latex_escape(label)} & "
            f"{detected_cell(d_detected, d_total)} & "
            f"{detected_cell(o_detected, o_total)} \\\\"
        )

    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
            "",
        ]
    )
    out_path.write_text("\n".join(lines))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tools-evaluation-json", required=True, type=Path)
    parser.add_argument("--root-cause-table", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.root_cause_table.parent.mkdir(parents=True, exist_ok=True)
    write_root_cause_table(load_data(args.tools_evaluation_json), args.root_cause_table)


if __name__ == "__main__":
    main()
