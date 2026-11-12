# Survey Questions, Data, and Generated Artifacts

This directory contains the questionnaire sources, anonymized and aggregated survey responses, the analysis script, and the generated survey figures/tables used by the paper.
The tool experiments live in [`../experiments/`](../experiments/).

## Directory Layout

| Path              | Contents                                                                                                                           |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------|
| `questionnaires/` | LaTeX sources for the developer and auditor questionnaires.                                                                        |
| `responses/`      | Aggregated survey responses: `devs_aggregated.csv` and `auditors_aggregated.csv`. Individual responses are not published.          |
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

The questionnaires promised the participants that only aggregated results are published, so the repository contains no individual responses.
The anonymized and aggregated response files are:

| File                                | Description                                                |
|-------------------------------------|------------------------------------------------------------|
| `responses/devs_aggregated.csv`     | Aggregated developer responses (36 respondents).           |
| `responses/auditors_aggregated.csv` | Aggregated auditor responses (12 respondents).             |

They cover every multiple-choice question; answers to the free-text questions are not published.
Each row gives a `question`, an `answer`, the number of respondents who chose it (`count`), and the number who answered the question (`answered`).
Free-text answers to an "Other" option are counted as `Other`.
Table 6 reports arithmetic field errors and bit-decomposition errors as one class, so these two options form one row that counts the respondents who chose either.

## Generate Practitioner Survey Artifacts

Run these commands from the `surveys/` directory:

```bash
python3 scripts/practitioners_overview.py \
  --dev-csv responses/devs_aggregated.csv \
  --auditor-csv responses/auditors_aggregated.csv \
  --overview-used-tools-figure figures/practitioners_overview_used_tools.pdf \
  --overview-missing-tools-figure figures/practitioners_overview_missing_tools.pdf \
  --overview-tool-traits-figure figures/practitioners_overview_tool_traits.pdf

python3 scripts/practitioners_vulnerability_perceptions.py \
  --dev-csv responses/devs_aggregated.csv \
  --auditor-csv responses/auditors_aggregated.csv \
  --vulnerability-perceptions-table tables/practitioners_vulnerability_perceptions.tex
```

This generates the survey figure and table of the paper:

| Output                                               | Paper item | Contents                                                                                  |
|------------------------------------------------------|------------|-------------------------------------------------------------------------------------------|
| `figures/practitioners_overview_used_tools.pdf`      | Figure 5a  | Security tool categories used by developers and auditors.                                 |
| `figures/practitioners_overview_tool_traits.pdf`     | Figure 5b  | Tool traits that developers and auditors find important.                                  |
| `figures/practitioners_overview_missing_tools.pdf`   | Figure 5c  | Tool categories that respondents report as missing from the market.                       |
| `tables/practitioners_vulnerability_perceptions.tex` | Table 6    | Vulnerability classes rated hard to detect manually and adequately covered by tools.      |
