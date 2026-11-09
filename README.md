# ZKP Security Tools and Verification: Coverage, Effectiveness, Adoption, and Challenges

This repository contains the artifact package for our paper titled "ZKP Security Tools and Verification: Coverage, Effectiveness, Adoption, and Challenges".
It is organized around three components:

```text
├── zkhydra/     # Framework for running ZK security tools
├── zkbugs/      # Dataset of ZK vulnerabilities
└── surveys/     # Survey data, questionnaires, analysis scripts, figures, and tables
```

## Workflow Overview

The tool is best understood as an orchestration layer for several Circom security analysis tools.
Instead of manually running tools one by one, the tool provides a single workflow in which the user provides a Circom circuit or a dataset of Circom bugs, selects the tools to run, and lets the framework execute the analyses consistently.
Its main target is `.circom` circuits, and the repository includes example circuits and support for running against the extended dataset, which contains real-world ZKP vulnerabilities.

In *isolated mode* (the `direct` flag value below), the analysis is run on a specific `.circom` circuit file.
This mode is typically used when the vulnerable circuit is already known or suspected.
Because the tool receives the relevant circuit directly, its analysis scope is narrow and focused, making it easier to identify the vulnerability.
The tool only needs to inspect the selected circuit and report any security-related findings.

In *project mode* (the `original` flag value below), the analysis starts from a broader project entry point rather than from the vulnerable circuit itself.
In this case, the tool must analyze the surrounding project structure, follow imports or dependencies, and determine which parts of the code are relevant.
This makes the analysis more challenging because the vulnerability may be hidden within a larger codebase rather than provided as an isolated input.

The main difference between the two modes is therefore the scope of analysis.
Isolated mode gives the tool a focused target and is useful for testing whether a tool can detect a known vulnerability.
Project mode is closer to a real audit scenario, where the exact location of the bug may not be known in advance.
As a result, project mode is generally harder, but it provides a more realistic view of how well the tool performs on complete projects.

The output analysis is based on collecting the raw results from each tool and determining whether each result contains a meaningful finding for the target circuit or bug case.
This is done by parsing each tool's output and comparing the reported findings against the ground truth defined in the extended dataset.
Results that cannot be matched automatically are reported as `Undecided` and are decided manually by the authors (see *Raw results* below).

## Running the Evaluation Tool on the Extended Dataset

### Step 0: Initialize Submodules

Initialize all needed submodules:

```bash
git submodule update --init
git submodule update --init --recursive zkhydra/
```

### Step 1: Build the Local Docker Image

Run from the repository root:

```bash
docker build -t zkhydra:local ./zkhydra
```

### Step 1.5: Download Project Codebases (required for project mode)

Isolated mode (the `direct` flag value) runs on the wrapper circuits already included in this repository (`.circom` files that instantiate the vulnerable part), so it needs no extra setup.
Project mode (the `original` flag value), however, requires the full project codebases to analyze.
Hence, before running `--zkbugs-mode original` or `both`, download them once:

```bash
docker run --rm \
  -v "$(pwd)/zkbugs:/zkhydra/zkbugs" \
  -w /zkhydra/zkbugs \
  zkhydra:local \
  bash scripts/download_sources.sh
```

This clones each project at its vulnerable commit into `zkbugs/dataset/codebases/` applies compatibility patches and runs the npm installs (a few GB; some stale repos may fail to compile, which is expected).
The mounted `zkbugs` makes the downloaded codebases visible to the evaluation run in the next step.

### Step 2: Run the Full Dataset Evaluation

This command evaluates every runnable Circom bug in the extended dataset included in this repository using the five tools of the paper:

```bash
docker run --rm \
  -v "$(pwd)/zkhydra/output:/zkhydra/output" \
  -v "$(pwd)/zkbugs:/zkhydra/zkbugs" \
  zkhydra:local \
  uv run python -m zkhydra.main zkbugs \
    --dataset zkbugs/dataset/circom \
    --zkbugs-mode both \
    --tools circomspect,circom_civer,picus,zkfuzz,conscs \
    --jobs 4 \
    --timeout 600 \
    --log-file \
    --output output/zkbugs-run
```

This writes results to `zkhydra/output/zkbugs-run/`.

### Step 3: Print the Summary

After the run finishes, print the aggregate results with Docker:

```bash
docker run --rm \
  -v "$(pwd)/zkhydra/output:/zkhydra/output" \
  -v "$(pwd)/zkhydra/scripts:/zkhydra/scripts:ro" \
  zkhydra:local \
  python3 scripts/print_zkbugs_summary.py output/zkbugs-run
```

The most relevant flags are:

| Flag                               | Meaning                                                                                                   |
|------------------------------------|-----------------------------------------------------------------------------------------------------------|
| `--dataset`                        | Path to the Circom portion of the extended dataset.                                                       |
| `--zkbugs-mode direct`             | Isolated mode: run each isolated vulnerable wrapper circuit.                                              |
| `--zkbugs-mode original`           | Project mode: run the full project entrypoints where available.                                           |
| `--zkbugs-mode both`               | Run isolated and project mode, skipping project cases that are identical to the isolated one.             |
| `--tools`                          | Comma-separated tools to run (`all` runs every supported tool).                                          |
| `--jobs`                           | Number of bugs to evaluate in parallel.                                                                   |
| `--timeout`                        | Per-tool timeout in seconds.                                                                              |
| `--output`                         | Output directory, relative to `zkhydra/` inside the container or host checkout.                           |

### Raw results and rebuilding the tool-evaluation summary

Figure 2 and Table IV are produced from a post-processed summary, `surveys/public/dataset/tools-evaluation.json`, which is already present in this repository. 
Regenerating the figures (see *Generate Tool-Evaluation Figure and Table* below) uses this summary and therefore requires no download and no evaluation run.

The summary is itself built from the per-tool raw results of both experiments, which can be obtained via the following link:

- **Raw results zip:** https://drive.google.com/file/d/1yma0B--pj30qsoZ8dmByYjAy8aALzMsI/view

The zip expands to `./results/`:

```text
results/
├── tp/                   # main experiment on the extended dataset (zkhydra `zkbugs` mode)
│   ├── summary.json
│   ├── isolated/<bug>/   # isolated mode (zkhydra writes it as direct/)
│   └── project/<bug>/    # project mode (zkhydra writes it as original/)
└── fp/                   # false-positive experiment (zkhydra `fp` mode)
    ├── summary.json
    └── <circuit>/
```

Each `<bug>/<tool>/` folder holds the tool's raw output (`raw.txt`), its parsed findings (`parsed.json`, `results.json`), and the verdict against the ground truth (`evaluation.json`).
Verdicts the harness could not decide automatically have `"need_manual_analysis": true`; their final `status` was decided manually by the authors (`"manual_analysis": "Done"`).
Each `<circuit>/` folder holds `fp_candidates.json`, which splits each tool's alerts into soundness alerts and lint warnings, and per tool the raw output plus `fp_triage.json`, the authors' verdict (`FalsePositive`, `RealIssue`, or `Undecided`) for each soundness alert.

To rebuild the summary, download and extract the zip, then run the builder against it:

```bash
# From the repository root: download results.zip from the link above, then extract.
unzip results.zip

cd surveys
python3 scripts/build_tools_evaluation.py \
  --zkhydra-output-dir ../results/tp \
  --website-bugs-json public/dataset/bugs.json \
  --out-json public/dataset/tools-evaluation.json \
  --out-pdfs-dir public/dataset/tools-evaluation
```

This reads the raw results and regenerates `surveys/public/dataset/tools-evaluation.json` (plus PDFs) under `surveys/public/dataset/`.

## Running the False-Positive Experiment

The false-positive experiment runs the same tools on 25 circuits from 9 audited, battle-tested Circom projects and triages every soundness alert.
The project selection, pinned commits, and circuits are documented in [`zkhydra/fp_experiment/README.md`](zkhydra/fp_experiment/README.md).
Run from `zkhydra/`:

```bash
# 1. Clone each project at its pinned commit, install its dependencies, and compile-check every circuit
scripts/fp_docker.sh python3 scripts/install_fp_projects.py

# 2. Run the tools (needs at least 32 GB of RAM; takes one to two days)
scripts/fp_docker.sh uv run python -m zkhydra.main fp --dataset output/fp-corpus/dataset/circom \
    --tools circomspect,circom_civer,picus,zkfuzz,conscs --timeout 1800 --jobs 1 --output output/fp-run

# 3. Manually triage every soundness alert (interactive, resumable)
python3 scripts/review_fp_triage.py output/fp-run --dataset output/fp-corpus/dataset/circom

# 4. Print the per-tool report
python3 scripts/process_fp_results.py output/fp-run
```

The results of our run, including our verdicts, are in `results/fp/` of the raw results zip (see above).

## Analyzing the Surveys

All survey commands below are run from `surveys/`.

```bash
# cd surveys
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Build the Questionnaire PDFs

This step requires a LaTeX installation with `pdflatex`.

```bash
cd questionnaires
make
cd ..
```

The outputs are:

| Output                          | Description                  |
|---------------------------------|------------------------------|
| `questionnaires/developers.pdf` | Developer questionnaire PDF. |
| `questionnaires/auditors.pdf`   | Auditor questionnaire PDF.   |

### Generate Practitioner Survey Figures and Tables

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

### Generate Tool-Evaluation Figure and Table

`generate_rq2_figures.py` reads the tool-evaluation summary (`public/dataset/tools-evaluation.json`) and produces Figure 2 and Table IV.

```bash
python scripts/generate_rq2_figures.py \
--tools-evaluation-json public/dataset/tools-evaluation.json \
--tool-outcomes-figure figures/rq2_tool_outcomes.pdf \
--root-cause-table tables/rq2_root_cause_detection.tex
```

### Generate False-Positive Figure and Table

`generate_fp_figures.py` reads the false-positive results (`results/fp/` from the raw results zip, see above) and produces the false-positive figure and Table V.

```bash
python scripts/generate_fp_figures.py \
--fp-results-dir ../results/fp \
--fp-outcomes-figure figures/rq2_fp_outcomes.pdf \
--fp-table tables/rq2_fp_results.tex
```

## Paper Artifact Mapping

The paper uses the following generated artifacts:

| Paper item | Repository artifact                                          |
|------------|--------------------------------------------------------------|
| Figure 2   | `surveys/figures/rq2_tool_outcomes.pdf`                      |
| Figure 3a  | `surveys/figures/practitioners_overview_used_tools.pdf`      |
| Figure 3b  | `surveys/figures/practitioners_overview_tool_traits.pdf`     |
| Figure 3c  | `surveys/figures/practitioners_overview_missing_tools.pdf`   |
| Table IV   | `surveys/tables/rq2_root_cause_detection.tex`                |
| Table V    | `surveys/tables/rq2_fp_results.tex`                          |
| FP figure  | `surveys/figures/rq2_fp_outcomes.pdf`                        |
| Table VIII | `surveys/tables/practitioners_vulnerability_perceptions.tex` |

## Tool Selection

During our search for ZK security tools, we ended up with the overview shown in the table below:

| Tool Name                                 | Link                                                      | Supported DSLs       | Open Source | Selected | Paper / Blog Post                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|-------------------------------------------|-----------------------------------------------------------|----------------------|-------------|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Circomspect                               | [GitHub](https://github.com/trailofbits/circomspect)      | Circom               | Yes         | Yes      | [Blog Post](https://blog.trailofbits.com/2022/09/15/it-pays-to-be-circomspect/)                                                                                                                                                                                                                                                                                                                                                                                       |
| ZKAP                                      | [GitHub](https://github.com/whbjzzwjxq/ZKAP)              | Circom               | Yes         | No       | [Paper](https://www.usenix.org/conference/usenixsecurity24/presentation/wen)                                                                                                                                                                                                                                                                                                                                                                                          |
| Korrekt                                   | [GitHub](https://github.com/quantstamp/halo2-analyzer)    | halo2                | Yes         | No       | [Paper](https://eprint.iacr.org/2023/1051)                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Coda                                      | [GitHub](https://github.com/Veridise/coda)                | Circom               | Yes         | No       | [Paper](https://eprint.iacr.org/2023/547)                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Picus                                     | [GitHub](https://github.com/Veridise/Picus)               | Circom, GNARK (R1CS) | Yes         | Yes      | [Paper](https://eprint.iacr.org/2023/512)                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Ecne                                      | [GitHub](https://github.com/franklynwang/EcneProject)     | Circom (R1CS)        | Yes         | No       | NA                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| SNARKProbe                                | [GitHub](https://github.com/BARC-Purdue/SNARKProbe)       | R1CS                 | Yes         | No       | [Paper](https://link.springer.com/chapter/10.1007/978-3-031-54773-7_14)                                                                                                                                                                                                                                                                                                                                                                                               |
| Civer                                     | [GitHub](https://github.com/costa-group/circom_civer)     | Circom               | Yes         | Yes      | [Paper](https://ieeexplore.ieee.org/document/10646792)                                                                                                                                                                                                                                                                                                                                                                                                                |
| Gnark Lean Extractor                      | [GitHub](https://github.com/reilabs/gnark-lean-extractor) | Gnark                | Yes         | No       | NA                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| fAmulet                                   | NA                                                        | Polygon zkEVM        | No          | No       | [Paper](https://arxiv.org/pdf/2410.12210)                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Verification of zkWasm in Coq (zkwasm-fv) | [GitHub](https://github.com/CertiKProject/zkwasm-fv)      | zkWasm               | Yes         | No       | [Blog Post](https://www.certik.com/resources/blog/advanced-formal-verification-of-zero-knowledge-proof-blockchains), [Blog Post](https://www.certik.com/resources/blog/advanced-formal-verification-of-zkp-verifying-a-zk-instruction), [Blog Post](https://www.certik.com/resources/blog/advanced-formal-verification-of-zkp-a-tale-of-two-zk-bugs), [Blog Post](https://www.certik.com/resources/blog/advanced-formal-verification-of-zkp-how-zk-memory-was-proven) |
| Sierra Analyzer                           | [GitHub](https://github.com/FuzzingLabs/sierra-analyzer)  | Cairo                | Yes         | No       | NA                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Pilspector                                | [GitHub](https://github.com/Schaeff/pilspector/)          | PIL                  | Yes         | No       | NA                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| zkFuzz                                    | [GitHub](https://github.com/Koukyosyumei/zkFuzz)          | Circom               | Yes         | Yes      | [Paper](https://arxiv.org/abs/2504.11961)                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Garden                                    | [GitHub](http://github.com/formal-land/garden)            | Circom               | Yes         | No       | NA                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ConsCS                                    | [GitHub](https://github.com/jinan789/ConsCS)              | Circom               | Yes         | Yes      | [Paper](https://www.computer.org/csdl/proceedings-article/icse/2025/056900a737/251mHhOXS9i)                                                                                                                                                                                                                                                                                                                                                                           |
| Zequal                                    | NA                                                        | Circom               | No          | No       | [Paper](https://www.cs.utexas.edu/~isil/zequal.pdf)                                                                                                                                                                                                                                                                                                                                                                                                                   |
| AC<sup>4</sup>                            | NA                                                        | Circom               | No          | No       | [Paper](https://arxiv.org/abs/2403.15676)                                                                                                                                                                                                                                                                                                                                                                                                                             |
| R1CS solver                               | [GitHub](https://github.com/faulhornlabs/r1cs-solver)     | Circom (R1CS)        | Yes         | No       | TBD / NA                                                                                                                                                                                                                                                                                                                                                                                                                                                              |

Since most tools target the Circom DSL, we decided to focus our evaluation on this ecosystem.
From this subset, we further narrowed our selection to tools that are publicly available as open-source software.
When attempting to install and execute these tools, we encountered several issues: many failed to compile or could not be executed successfully.
As a result, we excluded these from further consideration.
Among the remaining tools, we prioritized those that could be executed automatically without requiring manual intervention.
Based on these criteria, we selected the following tools for inclusion in our evaluation framework:

- Circomspect
- Civer
- ConsCS
- Picus
- zkFuzz

Ecne also meets these criteria but is excluded: when it judges a circuit unsound, it can list thousands of potentially bad constraints, which makes its alerts impractical to triage.
