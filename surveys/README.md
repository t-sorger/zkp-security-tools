# Survey Questions, Data, and Generated Artifacts

This directory contains the questionnaire sources, filtered survey responses, the analysis script, and the generated survey figures/tables used by the paper.
The tool experiments live in [`../experiments/`](../experiments/).

## Directory Layout

| Path              | Contents                                                                                                                           |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------|
| `questionnaires/` | LaTeX sources for the developer and auditor questionnaires.                                                                        |
| `responses/`      | Filtered CSV survey responses: `devs.csv` and `auditors.csv`. Demographic answers and free-text practitioner answers are excluded. |
| `scripts/`        | `practitioners_overview.py` (Figure 5) and `practitioners_vulnerability_perceptions.py` (Table 6).                                 |
| `figures/`        | Generated PDF figures.                                                                                                             |
| `tables/`         | Generated LaTeX tables.                                                                                                            |

## Requirements

The scripts require Python 3.11 or newer and `matplotlib` (pinned in `requirements.txt`).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The questionnaire PDFs require a LaTeX installation with `pdflatex`.

## Questionnaires

The questionnaire sources are:

| Audience   | Source                          |
|------------|---------------------------------|
| Developers | `questionnaires/developers.tex` |
| Auditors   | `questionnaires/auditors.tex`   |

To build the questionnaire PDFs:

```bash
cd questionnaires
make
```

This writes:

| Output                          | Description                  |
|---------------------------------|------------------------------|
| `questionnaires/developers.pdf` | Developer questionnaire PDF. |
| `questionnaires/auditors.pdf`   | Auditor questionnaire PDF.   |

## Survey Responses

The filtered response files are:

| File                     | Description                                     |
|--------------------------|-------------------------------------------------|
| `responses/devs.csv`     | Developer survey responses used by the scripts. |
| `responses/auditors.csv` | Auditor survey responses used by the scripts.   |

## Generate Practitioner Survey Artifacts

Run these commands from the `surveys/` directory:

```bash
python3 scripts/practitioners_overview.py \
  --dev-csv responses/devs.csv \
  --auditor-csv responses/auditors.csv \
  --overview-used-tools-figure figures/practitioners_overview_used_tools.pdf \
  --overview-missing-tools-figure figures/practitioners_overview_missing_tools.pdf \
  --overview-tool-traits-figure figures/practitioners_overview_tool_traits.pdf

python3 scripts/practitioners_vulnerability_perceptions.py \
  --dev-csv responses/devs.csv \
  --auditor-csv responses/auditors.csv \
  --vulnerability-perceptions-table tables/practitioners_vulnerability_perceptions.tex
```

This generates the survey figure and table of the paper:

| Output                                               | Paper item | Contents                                                                                  |
|------------------------------------------------------|------------|-------------------------------------------------------------------------------------------|
| `figures/practitioners_overview_used_tools.pdf`      | Figure 5a  | Security tool categories used by developers and auditors.                                 |
| `figures/practitioners_overview_tool_traits.pdf`     | Figure 5b  | Tool traits that developers and auditors find important.                                  |
| `figures/practitioners_overview_missing_tools.pdf`   | Figure 5c  | Tool categories that respondents report as missing from the market.                       |
| `tables/practitioners_vulnerability_perceptions.tex` | Table 6    | Vulnerability classes rated hard to detect manually and adequately covered by tools.      |
