# ZKP Security Tools and Verification: Coverage, Effectiveness, Adoption, and Challenges

This repository is the artifact of our paper "ZKP Security Tools and Verification: Coverage, Effectiveness, Adoption, and Challenges".
It covers the paper's two empirical parts:

- **Tool experiments (RQ2).**
  We run five automated Circom security tools on 70 real-world vulnerabilities (true positives) and on 25 circuits from 9 audited projects (false positives).
  The repository contains the harness that runs the tools, the vulnerability dataset, the raw output of every run, the authors' verdicts, and the scripts that produce the figures and tables.
- **Practitioner survey (RQ4, RQ5).**
  We surveyed 48 ZKP developers and auditors.
  The repository contains the questionnaires, the filtered responses, and the analysis script.

All figures and tables can be regenerated from the data in this repository.

## Contents

1. [Installation](#installation)
2. [Repository Overview](#repository-overview)
3. [Tool Experiments](#tool-experiments)
   - [Tool Selection](#tool-selection)
   - [Main Experiment: Known Vulnerabilities](#main-experiment-known-vulnerabilities)
   - [False-Positive Experiment: Audited Projects](#false-positive-experiment-audited-projects)
4. [Practitioner Survey](#practitioner-survey)
5. [Re-running the Experiments](#re-running-the-experiments)
6. [Results and Verdicts](#results-and-verdicts)
7. [Reproducing the Paper's Figures and Tables](#reproducing-the-papers-figures-and-tables)

## Installation

```bash
git clone https://github.com/t-sorger/zkp-security-tools.git
cd zkp-security-tools
git submodule update --init
git submodule update --init --recursive --force zkhydra/
```

The submodules are needed only to re-run the experiments (see [Re-running the Experiments](#re-running-the-experiments)).
Don't use `git clone --recurse-submodules` or `git submodule update --init --recursive`: zkbugs has nested entries without URLs, which abort the run and leave zkhydra empty.
The `--force` above also repairs a zkhydra left empty by such a run.

## Repository Overview

```text
├── zkhydra/       # Harness that runs the security tools (submodule)
├── zkbugs/        # Dataset of real-world ZKP vulnerabilities (submodule)
├── experiments/   # Tool experiments: raw results, verdicts, analysis scripts, figures, and tables
└── surveys/       # Practitioner survey: questionnaires, responses, analysis script, figures, and tables
```

| Folder         | Role in the paper                          | Documentation                                                                                              |
|----------------|--------------------------------------------|------------------------------------------------|
| `zkhydra/`     | Runs the tools in both experiments         | [zkhydra/README.md](zkhydra/README.md)         |
| `zkbugs/`      | The vulnerabilities of the main experiment | [zkbugs/README.md](zkbugs/README.md)           |
| `experiments/` | Figure 2, Table 4, Figure 3                | [experiments/README.md](experiments/README.md) |
| `surveys/`     | Figure 5, Table 6                          | [surveys/README.md](surveys/README.md)         |

## Tool Experiments

Both experiments use the same five tools and the same harness, [zkhydra](zkhydra/README.md).
For every run, zkhydra prepares the circuit, runs the tool with a timeout, stores its raw output, and parses its findings into a unified format.
The **main experiment** measures whether a tool detects a known vulnerability (true positives).
The **false-positive experiment** runs the same tools on audited, battle-tested projects and triages every alert they raise.

### Tool Selection

We focus on Circom: it is the language that most automated ZKP security tools target, and one of the most mature and widely deployed ZK DSLs.
During our search for ZKP security tools, we compiled the following overview:

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
| R1CS solver                               | [GitHub](https://github.com/faulhornlabs/r1cs-solver)     | Circom (R1CS)        | Yes         | No       | NA                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

From the Circom tools, we selected *all* that are open source, could be built and run, and need no user input such as properties or specifications.
Several tools failed to compile or could not be executed, and were excluded.
For tools with optional specification-driven modes, we use only the modes that need no manual annotations.
This gives five tools:

| Tool        | Technique                                                       | Repository                                                              |
|-------------|-----------------------------------------------------------------|-------------------------------------------------------------------------|
| Picus       | Symbolic verification (SMT) of under-constrained signals        | [Veridise/Picus](https://github.com/Veridise/Picus)                     |
| Civer       | Formal verification of templates against safety properties      | [costa-group/circom_civer](https://github.com/costa-group/circom_civer) |
| Circomspect | Static analysis (linter for known anti-patterns)                | [trailofbits/circomspect](https://github.com/trailofbits/circomspect)   |
| zkFuzz      | Fuzzing for unsoundness counterexamples                         | [Koukyosyumei/zkFuzz](https://github.com/Koukyosyumei/zkFuzz)           |
| ConsCS      | Constraint-based symbolic analysis of under-constrained signals | [jinan789/ConsCS](https://github.com/jinan789/ConsCS)                   |

### Main Experiment: Known Vulnerabilities

**Dataset.**
The dataset of Chaliasos et al. ([*SoK: What Don't We Know? Understanding Security Vulnerabilities in SNARKs*](https://www.usenix.org/system/files/usenixsecurity24-chaliasos.pdf), USENIX Security 2024) contains 29 real-world Circom vulnerabilities.
We extend it to 70 by adding the high- and critical-severity vulnerabilities disclosed in audit reports and security disclosures of deployed projects and their libraries, since CVEs and issue trackers rarely exist in this field.
Findings reported in multiple sources were deduplicated, and each root cause was derived from the reports and fixes.
The 70 bugs span 27 projects and come from 22 audits (60 bugs), 6 advisories (8 bugs), and 2 community bug trackers (2 bugs).
The dataset is the [`zkbugs`](zkbugs/README.md) submodule (`dataset/circom/`); [experiments/README.md](experiments/README.md#main-experiment-the-70-bugs) lists all 70 bugs.

**Isolated and project mode.**
For each bug, the dataset provides a minimal wrapper circuit that instantiates the vulnerable code and, when available, the vulnerable commit of the original project.
This lets us run each tool in two settings:

- In **isolated mode** (zkhydra: `--zkbugs-mode direct`), the tool analyzes the wrapper.
  The analysis scope is narrow, as when a vulnerable circuit is already known or suspected.
  All 70 bugs compile in this mode.
- In **project mode** (zkhydra: `--zkbugs-mode original`), the tool starts from the project's own entry point and has to analyze the surrounding codebase, as in a real audit where the location of the bug is unknown.
  56 bugs compile in this mode; the other projects fail because of stale code or deprecated dependencies.

**Verdicts.**
Each run is labeled detected (true positive), missed (false negative), error, or timeout.
zkhydra decides detected and missed by comparing the tool's findings with the dataset annotation.
A detection requires evidence tied to the annotated root cause:

- a counterexample that exercises the vulnerability (Picus, zkFuzz, ConsCS);
- an unsafe verdict on the vulnerable component (Civer);
- a warning on the root-cause lines (Circomspect).

When a tool reports a vulnerability but its output does not identify the ground-truth location, zkhydra marks the run as undecided, and two authors independently inspect the raw output and compare it with the dataset annotation before assigning the final label.
This was needed for 39 of the 65 true positives across both modes, all from Picus and zkFuzz, whose outputs lack source locations.
There were no disagreements.

**Setup.**
600-second timeout per tool and bug, 4 bugs in parallel, on a virtual machine with 8 vCPUs, 32 GB RAM, and an AMD EPYC-Milan CPU at 2.4 GHz.

### False-Positive Experiment: Audited Projects

Audited code has been reviewed by security experts and is expected to be largely bug-free, so alerts on it are most likely false alarms.

**Project selection.** A project is included if it meets all four criteria:

1. Its Circom circuits are open source.
2. At least one public third-party security audit covers the circuits.
3. It is battle-tested: deployed in production, or a library used by deployed circuits.
4. Its circuits compile with Circom 2.2.3, the latest release at the time of the experiment.

We rank the eligible projects by GitHub stars (snapshot of 2026-11-05) and pin each one to the first commit that includes the audit fixes, so that we analyze the audited code before any later, unaudited changes.

**Circuit selection.**
For applications, we analyze their top-level circuits (`component main`) with the parameters used in production.
Libraries only provide reusable templates, so we analyze the test circuits in their repositories that instantiate the audited templates.
Circuits with more than 10 million constraints are left out for resource reasons.
Two projects need small patches that do not change circuit semantics:

- [`tornado-core-circom2-port.patch`](zkhydra/fp_experiment/patches/tornado-core-circom2-port.patch) is a syntax-only port of tornado-core's circom 0.x code to circom 2.
- [`privacy-pools-core-mains.patch`](zkhydra/fp_experiment/patches/privacy-pools-core-mains.patch) adds the two main files that the project instantiates in its own `src/index.ts`.

This gives 25 circuits from 9 projects:

| Project                                                              | Stars | Audit(s)                                                                                                                                                                                                                                          | Pinned commit | Circuits (constraints)                                                                                                     |
|----------------------------------------------------------------------|------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|----------------------------------------------------------------------------------------------------------------------------|
| [tornado-core](https://github.com/tornadocash/tornado-core)          | 1,680 | [ABDK 2019](https://github.com/abdk-consulting/audits/blob/main/tornado/Tornado_circuit_audit.pdf)                                                                                                                                                | `a533ad9ffb`  | withdraw (59,009)                                                                                                          |
| [self](https://github.com/selfxyz/self)                              | 1,267 | zkSecurity 2025 ([Jan](https://reports.zksecurity.xyz/reports/celo-self-audit/), [Jun](https://reports.zksecurity.xyz/reports/celo-self-audit-2/), [Sep](https://reports.zksecurity.xyz/reports/self-aadhaar-circuits/))                          | `b50a2892be`  | register-sha256-sha256-sha256-rsa-65537-4096 (3,314,606), dsc-sha256-rsa-65537-4096 (6,436,994), vc-and-disclose (225,194) |
| [semaphore](https://github.com/semaphore-protocol/semaphore)         | 1,095 | [Veridise 2023](https://semaphore.pse.dev/Semaphore_3.0.0_Audit.pdf)                                                                                                                                                                              | `1bb57ca607`  | semaphore-v3-20 (17,689)                                                                                                   |
| [circomlib](https://github.com/iden3/circomlib)                      |   751 | [Veridise 2022](https://veridise.com/wp-content/uploads/2024/11/VAR_EF_0xparc_Circom.pdf)                                                                                                                                                         | `cff5ab6288`  | poseidon3 (765), eddsaposeidon (21,246), smtverifier10 (12,582), lessthan (36), pedersen2 (8,127), babypbk (10,114)        |
| [maci](https://github.com/privacy-ethereum/maci)                     |   596 | HashCloak [2022](https://maci.pse.dev/audit_reports/202220930_Hashcloak_audit_report.pdf), [2026](https://maci.pse.dev/audit_reports/20260317_Hashcloak_audit_report.pdf)                                                                         | `4d0e3a35f9`  | maci-polljoining-10 (23,926), maci-messageprocessorqv-10-20-2 (2,244,412), maci-votetallyqv-10-1-2 (100,082)               |
| [zk-email-verify](https://github.com/zkemail/zk-email-verify)        |   435 | [yAcademy 2023](https://docs.zk.email/files/yacademy-zkemail-audit-report.pdf); [zkSecurity 2024](https://docs.zk.email/files/zk_email_zksecurity_audit.pdf); [Matter Labs 2024](https://docs.zk.email/files/matterlabs-zkemail-audit-report.pdf) | `9ed3769dc3`  | emailverifier (5,993,156), rsaverifier65537-121-17 (208,463), sha256bytes-640 (2,077,273), selectregexreveal-34-8 (1,416)  |
| [privacy-pools-core](https://github.com/0xbow-io/privacy-pools-core) |   136 | [Oxorio 2025](https://github.com/0xbow-io/privacy-pools-core/blob/main/audit/circuits_audit_oxorio.md)                                                                                                                                            | `8da36d5e21`  | withdraw (54,878), commitment (2,283)                                                                                      |
| [iden3-circuits](https://github.com/iden3/circuits)                  |    94 | [Trail of Bits 2024](https://github.com/trailofbits/publications/blob/master/reviews/2024-05-polygonlabs-iden3circuits-securityreview.pdf)                                                                                                        | `62b65d3cca`  | authv3-40-64 (164,860), credentialatomicqueryv3offchain-40-32-64 (196,801), linkedmultiquery-10-32-64 (644,027)            |
| [nocturne](https://github.com/nocturne-xyz/protocol)                 |    81 | [Zellic 2023](https://github.com/Zellic/publications/blob/master/Nocturne%20-%20Zellic%20Audit%20Report.pdf)                                                                                                                                      | `f66fd0274e`  | joinsplit (124,892), canonaddrsigcheck (35,226)                                                                            |

For each project, [experiments/README.md](experiments/README.md#false-positive-experiment-the-25-circuits) gives the audit reports, the deployment evidence, the main file of each circuit, and the known unfixed findings; [`projects.json`](zkhydra/fp_experiment/projects.json) also records why each commit was chosen.

**Known unfixed findings.**
Audited code is not guaranteed to be bug-free, so we also record the audit findings that were acknowledged but not fixed at the pinned commit.
An alert on one of them counts as a real issue, not a false positive.

**Alerts and verdicts.**
We treat soundness alerts (under-constrained, over-constrained, and computational issues) as candidate false positives.
Circomspect's lint warnings count only as review burden, and a Circomspect parser error marks the run as failed.
Two authors independently review every soundness alert against the circuit source and the known unfixed findings and label it a false positive or a real issue.
There were no disagreements.

**Setup.**
1,800-second timeout per tool and circuit, circom 2.2.3, and the zkhydra Docker image, with one circuit at a time in a container capped at 24 GB of memory without swap.
A tool that exceeds the memory cap is killed and counted as failed.
Runs that time out or fail are reported separately and are not counted as false positives.

## Practitioner Survey

We designed two questionnaire variants, one for developers and researchers building ZKP systems and one for security practitioners auditing them, covering security tool usage, perceived tooling gaps, formal verification workflows, and LLM-assisted security practices.
Both were anonymous, and all questions were optional.
We contacted 200 practitioners and received 48 responses (36 developers, 12 auditors), a response rate of 24%.

[`surveys/`](surveys/README.md) contains:

- the LaTeX sources of both questionnaires (`questionnaires/`);
- the filtered responses (`responses/devs.csv`, `responses/auditors.csv`), from which demographic and free-text answers are removed;
- the analysis scripts that produce Figure 5 (`scripts/practitioners_overview.py`) and Table 6 (`scripts/practitioners_vulnerability_perceptions.py`).

How to run it is described in [Figures and Tables of the Survey](#figures-and-tables-of-the-survey).

## Re-running the Experiments

This repeats both experiments from scratch.
It is optional: the figures and tables can be reproduced from the stored results (see [Reproducing the Paper's Figures and Tables](#reproducing-the-papers-figures-and-tables)).
It needs an x86-64 machine with Docker; the false-positive experiment needs at least 32 GB of RAM and takes one to two days.
Initialize the submodules first (see [Installation](#installation)).

### Main Experiment

All commands run from the repository root.

1. Build the zkhydra Docker image:

   ```bash
   docker build -t zkhydra:local ./zkhydra
   ```

2. Download the project codebases (needed for project mode only).
   This clones each project at its vulnerable commit into `zkbugs/dataset/codebases/`, applies compatibility patches, and runs the npm installs (a few GB; some stale repos fail to compile, which is expected):

   ```bash
   docker run --rm \
     -v "$(pwd)/zkbugs:/zkhydra/zkbugs" \
     -w /zkhydra/zkbugs \
     zkhydra:local \
     bash scripts/download_sources.sh
   ```

3. Run the five tools on every runnable bug in both modes:

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

   This writes the results to `zkhydra/output/zkbugs-run/{direct,original}/`, the same layout as `experiments/results/tp/{isolated,project}/`.

4. Print the summary of each mode:

   ```bash
   docker run --rm \
     -v "$(pwd)/zkhydra/output:/zkhydra/output" \
     -v "$(pwd)/zkhydra/scripts:/zkhydra/scripts:ro" \
     zkhydra:local \
     python3 scripts/print_zkbugs_summary.py output/zkbugs-run/direct
   ```

   and the same with `output/zkbugs-run/original` for project mode.

5. Review the `Undecided` verdicts manually, as described in [zkhydra/README.md](zkhydra/README.md).

The most relevant flags of step 3:

| Flag                     | Meaning                                                                                 |
|--------------------------|-----------------------------------------------------------------------------------------|
| `--dataset`              | Path to the Circom part of the dataset.                                                 |
| `--zkbugs-mode direct`   | Isolated mode: run each bug's wrapper circuit.                                          |
| `--zkbugs-mode original` | Project mode: run the project's own entry point, where available.                       |
| `--zkbugs-mode both`     | Run both modes, skipping project-mode runs that would be identical to the isolated one. |
| `--tools`                | Comma-separated tools to run (`all` runs every tool zkhydra supports).                  |
| `--jobs`                 | Number of bugs evaluated in parallel.                                                   |
| `--timeout`              | Timeout per tool and bug, in seconds.                                                   |
| `--output`               | Output directory, relative to `zkhydra/`.                                               |

### False-Positive Experiment

All commands run from `zkhydra/`; [zkhydra/fp_experiment/README.md](zkhydra/fp_experiment/README.md) documents them in detail.

```bash
cd zkhydra

# 1. Clone each project at its pinned commit, install its dependencies, and compile-check every circuit
scripts/fp_docker.sh python3 scripts/install_fp_projects.py

# 2. Run the five tools on all 25 circuits
scripts/fp_docker.sh uv run python -m zkhydra.main fp --dataset output/fp-corpus/dataset/circom \
    --tools circomspect,circom_civer,picus,zkfuzz,conscs --timeout 1800 --jobs 1 --output output/fp-run

# 3. Triage every soundness alert manually (interactive, resumable)
python3 scripts/review_fp_triage.py output/fp-run --dataset output/fp-corpus/dataset/circom

# 4. Print the per-tool report
python3 scripts/process_fp_results.py output/fp-run
```

This writes the results to `zkhydra/output/fp-run/`, the same layout as `experiments/results/fp/`.

## Results and Verdicts

The raw results of both experiments are in [`experiments/results/`](experiments/results):

```text
experiments/results/
├── tp/                   # main experiment (zkhydra `zkbugs` mode)
│   ├── summary.json
│   ├── isolated/<bug>/   # isolated mode (zkhydra writes it as direct/)
│   └── project/<bug>/    # project mode (zkhydra writes it as original/)
└── fp/                   # false-positive experiment (zkhydra `fp` mode)
    ├── summary.json
    └── <project>__<circuit>/
```

Each `<bug>/<tool>/` folder holds the tool's raw output (`raw.txt`), its parsed findings (`parsed.json`, `results.json`), and the verdict against the ground truth (`evaluation.json`).
Verdicts that zkhydra could not decide automatically have `"need_manual_analysis": true`; their final `status` was decided by the authors (`"manual_analysis": "Done"`).
Each `<project>__<circuit>/` folder holds `fp_candidates.json`, which splits each tool's alerts into soundness alerts and lint warnings, and, per tool, the raw output and `fp_triage.json`, the authors' verdict (`FalsePositive`, `RealIssue`, or `Undecided`) for each soundness alert.
[experiments/README.md](experiments/README.md#result-files) describes every file.

## Reproducing the Paper's Figures and Tables

This needs Python 3.11 or newer and, for the questionnaire PDFs, a LaTeX installation with `pdflatex`.

| Paper item | Script                                                       | Generated file                                               |
|------------|--------------------------------------------------------------|--------------------------------------------------------------|
| Figure 2   | `experiments/scripts/rq2_tool_outcomes.py`                   | `experiments/figures/rq2_tool_outcomes.pdf`                  |
| Table 4    | `experiments/scripts/rq2_root_cause_detection.py`            | `experiments/tables/rq2_root_cause_detection.tex`            |
| Figure 3   | `experiments/scripts/rq2_fp_outcomes.py`                     | `experiments/figures/rq2_fp_outcomes.pdf`                    |
| Figure 5a  | `surveys/scripts/practitioners_overview.py`                  | `surveys/figures/practitioners_overview_used_tools.pdf`      |
| Figure 5b  | `surveys/scripts/practitioners_overview.py`                  | `surveys/figures/practitioners_overview_tool_traits.pdf`     |
| Figure 5c  | `surveys/scripts/practitioners_overview.py`                  | `surveys/figures/practitioners_overview_missing_tools.pdf`   |
| Table 6    | `surveys/scripts/practitioners_vulnerability_perceptions.py` | `surveys/tables/practitioners_vulnerability_perceptions.tex` |

### Figures and Tables of the Tool Experiments

```bash
cd experiments
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 1. Summary of the main experiment, from the raw results
python3 scripts/tools_evaluation.py \
--zkhydra-output-dir results/tp \
--website-bugs-json data/bugs.json \
--out-json data/tools-evaluation.json \
--out-pdfs-dir data/tools-evaluation

# 2. Figure 2
python3 scripts/rq2_tool_outcomes.py \
--tools-evaluation-json data/tools-evaluation.json \
--tool-outcomes-figure figures/rq2_tool_outcomes.pdf

# 3. Table 4
python3 scripts/rq2_root_cause_detection.py \
--tools-evaluation-json data/tools-evaluation.json \
--root-cause-table tables/rq2_root_cause_detection.tex

# 4. Figure 3
python3 scripts/rq2_fp_outcomes.py \
--fp-results-dir results/fp \
--fp-outcomes-figure figures/rq2_fp_outcomes.pdf

deactivate
cd ..
```

### Figures and Tables of the Survey

```bash
cd surveys
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Questionnaire PDFs: questionnaires/developers.pdf and questionnaires/auditors.pdf
(cd questionnaires && make)

# Figure 5
python3 scripts/practitioners_overview.py \
--dev-csv responses/devs.csv \
--auditor-csv responses/auditors.csv \
--overview-used-tools-figure figures/practitioners_overview_used_tools.pdf \
--overview-missing-tools-figure figures/practitioners_overview_missing_tools.pdf \
--overview-tool-traits-figure figures/practitioners_overview_tool_traits.pdf

# Table 6
python3 scripts/practitioners_vulnerability_perceptions.py \
--dev-csv responses/devs.csv \
--auditor-csv responses/auditors.csv \
--vulnerability-perceptions-table tables/practitioners_vulnerability_perceptions.tex

deactivate
cd ..
```
