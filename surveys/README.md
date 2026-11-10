# Survey Questions, Data, and Generated Artifacts

This directory contains the questionnaire sources, filtered survey responses, the analysis script, and the generated survey figures/tables used by the paper.
The tool experiments live in [`../experiments/`](../experiments/).

## Directory Layout

| Path              | Contents                                                                                                                           |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------|
| `questionnaires/` | LaTeX sources for the developer and auditor questionnaires.                                                                        |
| `responses/`      | Filtered CSV survey responses: `devs.csv` and `auditors.csv`. Demographic answers and free-text practitioner answers are excluded. |
| `scripts/`        | `generate_practitioner_artifacts.py`, which generates the survey figures and tables.                                               |
| `figures/`        | Generated PDF figures.                                                                                                             |
| `tables/`         | Generated LaTeX tables.                                                                                                            |

## Requirements

The script requires Python 3 and `matplotlib` (pinned in `requirements.txt`).

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

Run this command from the `surveys/` directory:

```bash
python scripts/generate_practitioner_artifacts.py \
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
```

This generates:

| Output                                               | Contents                                                                                 |
|------------------------------------------------------|------------------------------------------------------------------------------------------|
| `figures/practitioners_tool_categories.pdf`          | Security tool categories used by developers and auditors.                                |
| `figures/practitioners_frameworks.pdf`               | Languages and frameworks where respondents use security tools.                           |
| `figures/practitioners_tool_onboarding_effort.pdf`   | Integration/onboarding effort for security analysis and formal verification tools.       |
| `figures/practitioners_vulns_tool_gaps.pdf`          | Crucial vulnerability classes respondents report as unsupported by tools they have used. |
| `figures/practitioners_missing_market_tools.pdf`     | Tool categories respondents report as missing from the market.                           |
| `figures/practitioners_overview_used_tools.pdf`      | Compact overview panel for used tools.                                                   |
| `figures/practitioners_overview_missing_tools.pdf`   | Compact overview panel for missing tools.                                                |
| `figures/practitioners_overview_tool_traits.pdf`     | Compact overview panel for desired tool traits.                                          |
| `figures/practitioners_tool_characteristics.pdf`     | Full tool-characteristics figure.                                                        |
| `tables/practitioners_tool_characteristics.tex`      | Tool-characteristics LaTeX table.                                                        |
| `tables/practitioners_vulnerability_perceptions.tex` | Vulnerability perception LaTeX table.                                                    |

## Paper Artifact Mapping

The paper uses the following generated files:

| Paper item | Repository artifact                                  |
|------------|------------------------------------------------------|
| Figure 4a  | `figures/practitioners_overview_used_tools.pdf`      |
| Figure 4b  | `figures/practitioners_overview_tool_traits.pdf`     |
| Figure 4c  | `figures/practitioners_overview_missing_tools.pdf`   |
| Table 7    | `tables/practitioners_vulnerability_perceptions.tex` |
