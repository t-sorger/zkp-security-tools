# Experiments

This folder contains the two tool experiments of the paper (section *Tools' Effectiveness*): the raw results of every tool run, the authors' verdicts, and the scripts that turn them into the paper's figures and tables.
The main [README](../README.md) explains how the tools, bugs, and projects were selected and how to run everything.
This file is the detailed reference: which bugs and circuits were analyzed, what each result file contains, and which numbers a reproduction must give.

## Contents

| Path                                  | Contents                                                                                          |
|---------------------------------------|---------------------------------------------------------------------------------------------------|
| `results/tp/`                         | Raw results of the main experiment (known vulnerabilities), produced by zkhydra's `zkbugs` mode.  |
| `results/fp/`                         | Raw results of the false-positive experiment (audited projects), produced by zkhydra's `fp` mode. |
| `data/tools-evaluation.json`          | Post-processed summary of `results/tp/`, the input of Figure 2 and Table 4.                       |
| `data/bugs.json`                      | Bug metadata from the zkbugs website, used to link each bug to its website entry.                 |
| `scripts/tools_evaluation.py`         | Builds `data/tools-evaluation.json` from `results/tp/`.                                           |
| `scripts/rq2_tool_outcomes.py`        | Figure 2, from `data/tools-evaluation.json`.                                                      |
| `scripts/rq2_root_cause_detection.py` | Table 4, from `data/tools-evaluation.json`.                                                       |
| `scripts/rq2_fp_outcomes.py`          | Figure 3, from `results/fp/`.                                                                     |
| `figures/`, `tables/`                 | Generated outputs (not tracked).                                                                  |

The commands are in the main README, under [Reproducing the Paper's Figures and Tables](../README.md#reproducing-the-papers-figures-and-tables).

## Main Experiment: The 70 Bugs

The bugs come from the Circom part of the extended zkbugs dataset (submodule [`zkbugs/`](../zkbugs), `dataset/circom/`).
How the dataset was extended is described in the main README; the numbers are:

- 70 bugs from 27 projects: 60 bugs from 22 audit reports, 8 bugs from 6 advisories, and 2 bugs from 2 community bug trackers.
- Vulnerability: 60 under-constrained, 6 computational issues, 3 over-constrained, 1 private information leakage.
- Root cause: 22 missing input constraints, 18 wrong translation of logic into constraints, 10 unsafe reuse of a circuit, 6 assigned but unconstrained, 6 circuit design issues, 4 arithmetic field issues, 3 misimplementations of a specification, 1 other programming error.
- All 70 bugs are run in *isolated* mode.
  56 of them are also run in *project* mode; the other 14 bugs have no project entry point in the dataset (`"Original Entrypoint": []`).

<details>
<summary>All 70 bugs (from <code>results/tp/isolated/*/ground_truth.json</code>)</summary>

| Bug                                                                                                                                    | Project                                                                                                   | Vulnerability               | Root cause                                  | Source       | Project mode |
|----------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|-----------------------------|---------------------------------------------|--------------|--------------|
| Missing range checks in BigMod                                                                                                         | [0xbok/circom-bigint](https://github.com/0xbok/circom-bigint)                                             | Under-Constrained           | Arithmetic Field Issues                     | Audit report | yes          |
| Base64DecodedLength output is declared but never constrained                                                                           | [aptos-labs/keyless-zk-proofs](https://github.com/aptos-labs/keyless-zk-proofs)                           | Under-Constrained           | Assigned but Unconstrained                  | Advisory     | yes          |
| CreditNoteProofs can be stolen                                                                                                         | [Arianee/arianee-sdk](https://github.com/Arianee/arianee-sdk)                                             | Under-Constrained           | Missing Input Constraints                   | Audit report | yes          |
| OwnershipProofs could identify issuers                                                                                                 | [Arianee/arianee-sdk](https://github.com/Arianee/arianee-sdk)                                             | Under-Constrained           | Missing Input Constraints                   | Audit report | yes          |
| Blake3NovaTreePath_CheckDepth LessThan/GreaterEqThan missing range checks                                                              | [banyancomputer/hot-proofs-blake3-circom](https://github.com/banyancomputer/hot-proofs-blake3-circom)     | Under-Constrained           | Missing Input Constraints                   | Advisory     | yes          |
| Dark Forest v0.3: Missing Bit Length Check                                                                                             | [darkforest-eth/darkforest-v0.3](https://github.com/darkforest-eth/darkforest-v0.3)                       | Under-Constrained           | Unsafe Reuse of Circuit                     | Bug tracker  | yes          |
| Decoder accepting bogus output signal                                                                                                  | [iden3/circomlib](https://github.com/iden3/circomlib)                                                     | Under-Constrained           | Wrong Translation of Logic into Constraints | Audit report | no           |
| MiMC Hash: Assigned but not Constrained                                                                                                | [iden3/circomlib](https://github.com/iden3/circomlib)                                                     | Under-Constrained           | Assigned but Unconstrained                  | Bug tracker  | no           |
| Underconstrained outputs in BitElementMulAny                                                                                           | [iden3/circomlib](https://github.com/iden3/circomlib)                                                     | Under-Constrained           | Unsafe Reuse of Circuit                     | Audit report | no           |
| Underconstrained outputs in Window4                                                                                                    | [iden3/circomlib](https://github.com/iden3/circomlib)                                                     | Under-Constrained           | Unsafe Reuse of Circuit                     | Audit report | no           |
| Underconstrained outputs in WindowMulFix                                                                                               | [iden3/circomlib](https://github.com/iden3/circomlib)                                                     | Under-Constrained           | Unsafe Reuse of Circuit                     | Audit report | no           |
| Underconstrained points in Edwards2Montgomery                                                                                          | [iden3/circomlib](https://github.com/iden3/circomlib)                                                     | Under-Constrained           | Missing Input Constraints                   | Audit report | no           |
| Underconstrained points in Montgomery2Edwards                                                                                          | [iden3/circomlib](https://github.com/iden3/circomlib)                                                     | Under-Constrained           | Missing Input Constraints                   | Audit report | no           |
| Underconstrained points in MontgomeryAdd                                                                                               | [iden3/circomlib](https://github.com/iden3/circomlib)                                                     | Under-Constrained           | Missing Input Constraints                   | Audit report | no           |
| Underconstrained points in MontgomeryDouble                                                                                            | [iden3/circomlib](https://github.com/iden3/circomlib)                                                     | Under-Constrained           | Missing Input Constraints                   | Audit report | no           |
| Unsafe use of Num2Bits in multiple circuits                                                                                            | [iden3/circuits](https://github.com/iden3/circuits)                                                       | Under-Constrained           | Wrong Translation of Logic into Constraints | Audit report | no           |
| Clamp LessThan inputs are not range-checked                                                                                            | [inference-labs-inc/subnet-2-circom](https://github.com/inference-labs-inc/subnet-2-circom)               | Under-Constrained           | Missing Input Constraints                   | Advisory     | yes          |
| Subtract uses an unconstrained multiplier d                                                                                            | [inference-labs-inc/subnet-2-circom](https://github.com/inference-labs-inc/subnet-2-circom)               | Under-Constrained           | Assigned but Unconstrained                  | Advisory     | yes          |
| Mismatched Base64url Decoding May Break Completeness                                                                                   | [Moonsong-Labs/zksync-social-login-circuit](https://github.com/Moonsong-Labs/zksync-social-login-circuit) | Over-Constrained            | Misimplementation of a Specification        | Audit report | yes          |
| Non-Determinism of Some Inputs                                                                                                         | [Moonsong-Labs/zksync-social-login-circuit](https://github.com/Moonsong-Labs/zksync-social-login-circuit) | Under-Constrained           | Missing Input Constraints                   | Audit report | yes          |
| Babyjubjub Suborder Constraints Not Applied Correctly                                                                                  | [pantherfoundation/panther-core](https://github.com/pantherfoundation/panther-core)                       | Under-Constrained           | Missing Input Constraints                   | Audit report | yes          |
| Blacklist States Cannot Be Represented Within the Circom Field                                                                         | [pantherfoundation/panther-core](https://github.com/pantherfoundation/panther-core)                       | Computational Issues        | Arithmetic Field Issues                     | Audit report | yes          |
| Bypassing internal transfer limits via swaps                                                                                           | [pantherfoundation/panther-core](https://github.com/pantherfoundation/panther-core)                       | Under-Constrained           | Wrong Translation of Logic into Constraints | Audit report | yes          |
| Data Escrow Encrypted Message Constructed From Incorrect Input                                                                         | [pantherfoundation/panther-core](https://github.com/pantherfoundation/panther-core)                       | Computational Issues        | Other Programming Errors                    | Audit report | yes          |
| KYT Signature Verification Process Fails for Any Non-Zero Signed Message Hash                                                          | [pantherfoundation/panther-core](https://github.com/pantherfoundation/panther-core)                       | Over-Constrained            | Wrong Translation of Logic into Constraints | Audit report | yes          |
| Nullifier Verification Can Be Disabled in ZSwapV1                                                                                      | [pantherfoundation/panther-core](https://github.com/pantherfoundation/panther-core)                       | Under-Constrained           | Circuit Design Issue                        | Audit report | yes          |
| Unsafe Use of Num2Bits(254) on Blacklist Leaf                                                                                          | [pantherfoundation/panther-core](https://github.com/pantherfoundation/panther-core)                       | Under-Constrained           | Missing Input Constraints                   | Audit report | yes          |
| Zone Related Limits Can Be Bypassed in ZSwapV1                                                                                         | [pantherfoundation/panther-core](https://github.com/pantherfoundation/panther-core)                       | Under-Constrained           | Wrong Translation of Logic into Constraints | Audit report | yes          |
| ZoneIdInclusionProver Check Can Be Bypassed                                                                                            | [pantherfoundation/panther-core](https://github.com/pantherfoundation/panther-core)                       | Under-Constrained           | Missing Input Constraints                   | Audit report | yes          |
| forTxReward Gets Abstracted Away in the Reward Calculation                                                                             | [pantherfoundation/panther-core](https://github.com/pantherfoundation/panther-core)                       | Computational Issues        | Wrong Translation of Logic into Constraints | Audit report | yes          |
| zAccountRenewalV1 Can Validate Multiple Nullifiers for the Same UTXO Commitment                                                        | [pantherfoundation/panther-core](https://github.com/pantherfoundation/panther-core)                       | Under-Constrained           | Missing Input Constraints                   | Audit report | yes          |
| zAccountRenewalV1 Circuit Does Not Validate KYC Certificates for Expiry                                                                | [pantherfoundation/panther-core](https://github.com/pantherfoundation/panther-core)                       | Under-Constrained           | Missing Input Constraints                   | Audit report | yes          |
| Input signal s is not constrained in eff_ecdsa.circom                                                                                  | [personaelabs/spartan-ecdsa](https://github.com/personaelabs/spartan-ecdsa)                               | Under-Constrained           | Missing Input Constraints                   | Audit report | yes          |
| Knowledge of any member signature allow to generate proof of membership                                                                | [personaelabs/spartan-ecdsa](https://github.com/personaelabs/spartan-ecdsa)                               | Under-Constrained           | Circuit Design Issue                        | Audit report | yes          |
| Under constrained circuits compromising the soundness of the system                                                                    | [personaelabs/spartan-ecdsa](https://github.com/personaelabs/spartan-ecdsa)                               | Under-Constrained           | Assigned but Unconstrained                  | Audit report | yes          |
| Data are not fully verified during state update                                                                                        | [privacy-scaling-explorations/maci](https://github.com/privacy-scaling-explorations/maci)                 | Under-Constrained           | Misimplementation of a Specification        | Audit report | no           |
| Under-constrained DateEncoder remainder signals                                                                                        | [rarimo/passport-zk-circuits](https://github.com/rarimo/passport-zk-circuits)                             | Under-Constrained           | Missing Input Constraints                   | Advisory     | yes          |
| Spammers may slash themselves                                                                                                          | [Rate-Limiting-Nullifier/circom-rln](https://github.com/Rate-Limiting-Nullifier/circom-rln)               | Under-Constrained           | Circuit Design Issue                        | Audit report | yes          |
| Unsound Addition Gadget                                                                                                                | [reclaimprotocol/circom-chacha20](https://github.com/reclaimprotocol/circom-chacha20)                     | Under-Constrained           | Wrong Translation of Logic into Constraints | Audit report | no           |
| Unsound Left Rotation                                                                                                                  | [reclaimprotocol/circom-chacha20](https://github.com/reclaimprotocol/circom-chacha20)                     | Under-Constrained           | Wrong Translation of Logic into Constraints | Audit report | no           |
| Unsound XOR gadget                                                                                                                     | [reclaimprotocol/circom-chacha20](https://github.com/reclaimprotocol/circom-chacha20)                     | Under-Constrained           | Wrong Translation of Logic into Constraints | Audit report | no           |
| An attacker can craft a fake non-inclusion proof for a given key due to an aliasing bug in the SMT verifier                            | [selfxyz/self](https://github.com/selfxyz/self)                                                           | Under-Constrained           | Wrong Translation of Logic into Constraints | Audit report | yes          |
| Big Integer Zero-Check Is Not Sound                                                                                                    | [selfxyz/self](https://github.com/selfxyz/self)                                                           | Computational Issues        | Wrong Translation of Logic into Constraints | Audit report | yes          |
| Exclusion Check Of Forbidden Countries Is Unsound And Incomplete Due To Incorrect Indexing                                             | [selfxyz/self](https://github.com/selfxyz/self)                                                           | Computational Issues        | Wrong Translation of Logic into Constraints | Audit report | yes          |
| Forbidden Country Check Bypass via Packed Byte Overflow                                                                                | [selfxyz/self](https://github.com/selfxyz/self)                                                           | Under-Constrained           | Wrong Translation of Logic into Constraints | Audit report | yes          |
| Missing Byte Range Checks Allows Packed Data Pollution                                                                                 | [selfxyz/self](https://github.com/selfxyz/self)                                                           | Under-Constrained           | Wrong Translation of Logic into Constraints | Audit report | yes          |
| Missing boolean constraints in the Merkle tree path leads to an attacker being able to craft a fake Merkle proof for an arbitrary leaf | [selfxyz/self](https://github.com/selfxyz/self)                                                           | Under-Constrained           | Wrong Translation of Logic into Constraints | Audit report | yes          |
| Second Pre-Image Attacks On PackBytesAndPoseidon May Be Used To Register Arbitrary Passports And DSC Certificates                      | [selfxyz/self](https://github.com/selfxyz/self)                                                           | Under-Constrained           | Missing Input Constraints                   | Audit report | yes          |
| The registration and disclosure circuits lack range checks for the input indices                                                       | [selfxyz/self](https://github.com/selfxyz/self)                                                           | Under-Constrained           | Wrong Translation of Logic into Constraints | Audit report | yes          |
| No Zero Value Validation                                                                                                               | [semaphore-protocol/semaphore](https://github.com/semaphore-protocol/semaphore)                           | Under-Constrained           | Missing Input Constraints                   | Audit report | yes          |
| Private Information Leakage                                                                                                            | [sismo-core/hydra-s2-zkps](https://github.com/sismo-core/hydra-s2-zkps)                                   | Private Information Leakage | Circuit Design Issue                        | Audit report | yes          |
| EmitIfInRange LessThan missing range check on index                                                                                    | [siv-org/verifiable-private-overrides](https://github.com/siv-org/verifiable-private-overrides)           | Under-Constrained           | Missing Input Constraints                   | Advisory     | yes          |
| ExtractStringFromPoint shiftedFirstByte is assigned but not constrained                                                                | [siv-org/verifiable-private-overrides](https://github.com/siv-org/verifiable-private-overrides)           | Under-Constrained           | Assigned but Unconstrained                  | Advisory     | yes          |
| ArrayXOR is under constrained                                                                                                          | [succinctlabs/telepathy-circuits](https://github.com/succinctlabs/telepathy-circuits)                     | Under-Constrained           | Assigned but Unconstrained                  | Audit report | yes          |
| Incorrect handling of point doubling can allow signature forgery                                                                       | [succinctlabs/telepathy-circuits](https://github.com/succinctlabs/telepathy-circuits)                     | Under-Constrained           | Unsafe Reuse of Circuit                     | Audit report | yes          |
| Prover can lock user funds by including ill-formed BigInts in public key commitment                                                    | [succinctlabs/telepathy-circuits](https://github.com/succinctlabs/telepathy-circuits)                     | Under-Constrained           | Unsafe Reuse of Circuit                     | Audit report | yes          |
| Prover can lock user funds by supplying non-reduced Y values to G1BigIntToSignFlag                                                     | [succinctlabs/telepathy-circuits](https://github.com/succinctlabs/telepathy-circuits)                     | Under-Constrained           | Unsafe Reuse of Circuit                     | Audit report | yes          |
| Template CoreVerifyPubkeyG1 does not perform input validation (Simplified)                                                             | [succinctlabs/telepathy-circuits](https://github.com/succinctlabs/telepathy-circuits)                     | Under-Constrained           | Unsafe Reuse of Circuit                     | Audit report | yes          |
| Zero Padding for Sha256 in ExpandMessageXMD is vulnerable to an overflow                                                               | [succinctlabs/telepathy-circuits](https://github.com/succinctlabs/telepathy-circuits)                     | Under-Constrained           | Arithmetic Field Issues                     | Audit report | yes          |
| Incorrect Initialization in Membership Circuits                                                                                        | [tangle-network/protocol-solidity](https://github.com/tangle-network/protocol-solidity)                   | Computational Issues        | Wrong Translation of Logic into Constraints | Audit report | yes          |
| Missing Range Checks on Comparison Circuits                                                                                            | [Unirep/Unirep](https://github.com/Unirep/Unirep)                                                         | Under-Constrained           | Unsafe Reuse of Circuit                     | Audit report | yes          |
| Underconstrained Circuit allows Invalid Comparison                                                                                     | [Unirep/Unirep](https://github.com/Unirep/Unirep)                                                         | Under-Constrained           | Arithmetic Field Issues                     | Audit report | yes          |
| Spend missing range checks on GreaterEqThan inputs                                                                                     | [worm-privacy/proof-of-burn](https://github.com/worm-privacy/proof-of-burn)                               | Under-Constrained           | Missing Input Constraints                   | Advisory     | yes          |
| EmailAuth circuit doesn't work with specific email addresses and domain names                                                          | [zkemail/ether-email-auth](https://github.com/zkemail/ether-email-auth)                                   | Over-Constrained            | Circuit Design Issue                        | Audit report | yes          |
| SHA256 templates can be made return 0 on arbitrary inputs                                                                              | [zkemail/zk-email-verify](https://github.com/zkemail/zk-email-verify)                                     | Under-Constrained           | Missing Input Constraints                   | Audit report | yes          |
| Underconstrained FpMul circuit                                                                                                         | [zkemail/zk-email-verify](https://github.com/zkemail/zk-email-verify)                                     | Under-Constrained           | Missing Input Constraints                   | Audit report | yes          |
| Email spoofing via manipulated From header                                                                                             | [zkemail/zk-regex](https://github.com/zkemail/zk-regex)                                                   | Under-Constrained           | Misimplementation of a Specification        | Audit report | yes          |
| FromAddrRegex circuit allows for email address spoofing                                                                                | [zkemail/zk-regex](https://github.com/zkemail/zk-regex)                                                   | Under-Constrained           | Wrong Translation of Logic into Constraints | Audit report | yes          |
| Circuit Does Not Check the ERC-20 Sum Correctly                                                                                        | [zkopru-network/zkopru](https://github.com/zkopru-network/zkopru)                                         | Under-Constrained           | Circuit Design Issue                        | Audit report | yes          |
| Previously Correct Ownership Proof Disabled via Code Changes                                                                           | [zkopru-network/zkopru](https://github.com/zkopru-network/zkopru)                                         | Under-Constrained           | Unsafe Reuse of Circuit                     | Audit report | yes          |


</details>

## False-Positive Experiment: The 25 Circuits

The selection criteria are described in the main [README](../README.md#false-positive-experiment-audited-projects).
Every circuit is a unit in `results/fp/`, named `<project>__<circuit>`.
Shared libraries use [circomlib](https://github.com/iden3/circomlib) at `cff5ab6288b55ef23602221694a6a38a0239dcc0` (v2.0.5, the version the zkbugs dataset vendors).
[`zkhydra/fp_experiment/projects.json`](../zkhydra/fp_experiment/projects.json) holds the full record of each project, including why the commit was chosen, the scope of each audit, and the dependency installation steps; the two patches are in [`zkhydra/fp_experiment/patches/`](../zkhydra/fp_experiment/patches).

| Project                                                              | Pinned commit                              | Audit reports                                                                                                                                                                                                                                           | Deployment evidence                                                               | Known unfixed findings |
|----------------------------------------------------------------------|--------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|-----------------------:|
| [tornado-core](https://github.com/tornadocash/tornado-core)          | `a533ad9ffb62163a42d4fa9a09984c5dd4e5c41d` | [ABDK Consulting 2019-11](https://github.com/abdk-consulting/audits/blob/main/tornado/Tornado_circuit_audit.pdf)                                                                                                                                        | [source](https://etherscan.io/address/0x12D66f87A04A9E220743712cE6d9bB1B5616B8Fc) | 1                      |
| [self](https://github.com/selfxyz/self)                              | `b50a2892be3d61017eb14d27e0f34dd388c5bca1` | [zkSecurity 2025-01](https://reports.zksecurity.xyz/reports/celo-self-audit/), [zkSecurity 2025-06](https://reports.zksecurity.xyz/reports/celo-self-audit-2/), [zkSecurity 2025-09](https://reports.zksecurity.xyz/reports/self-aadhaar-circuits/)     | [source](https://cdn.jsdelivr.net/npm/@selfxyz/contracts@1.2.3/README.md)         | 7                      |
| [semaphore](https://github.com/semaphore-protocol/semaphore)         | `1bb57ca607afc21a85c73826c53fc768cbacc8a1` | [Veridise 2023-01](https://semaphore.pse.dev/Semaphore_3.0.0_Audit.pdf)                                                                                                                                                                                 | [source](https://docs.semaphore.pse.dev/V3/deployed-contracts)                    | 0                      |
| [circomlib](https://github.com/iden3/circomlib)                      | `cff5ab6288b55ef23602221694a6a38a0239dcc0` | [Veridise + 0xPARC Community + Ethereum Foundation 2022-11](https://veridise.com/wp-content/uploads/2024/11/VAR_EF_0xparc_Circom.pdf)                                                                                                                   | [source](https://www.npmjs.com/package/circomlib)                                 | 10                     |
| [maci](https://github.com/privacy-ethereum/maci)                     | `4d0e3a35f9f0c0122101050903bfcb383f7aaaa4` | [HashCloak 2026-03](https://maci.pse.dev/audit_reports/20260317_Hashcloak_audit_report.pdf), [HashCloak 2022-09](https://maci.pse.dev/audit_reports/202220930_Hashcloak_audit_report.pdf)                                                               | [source](https://maci.pse.dev/docs/supported-networks/deployed-contracts)         | 0                      |
| [zk-email-verify](https://github.com/zkemail/zk-email-verify)        | `9ed3769dc3d96fb0d7c45f1f014dcd9bfb63675b` | [yAcademy 2023](https://docs.zk.email/files/yacademy-zkemail-audit-report.pdf), [zkSecurity 2024-05](https://docs.zk.email/files/zk_email_zksecurity_audit.pdf), [Matter Labs 2024-10](https://docs.zk.email/files/matterlabs-zkemail-audit-report.pdf) | [source](https://docs.zk.email/account-recovery/deployed-contracts)               | 1                      |
| [privacy-pools-core](https://github.com/0xbow-io/privacy-pools-core) | `8da36d5e2150ab3c567d85ca8a6b2eb6b51740cb` | [Oxorio 2025-02](https://github.com/0xbow-io/privacy-pools-core/blob/main/audit/circuits_audit_oxorio.md)                                                                                                                                               | [source](https://etherscan.io/address/0xf241d57c6debae225c0f2e6ea1529373c9a9c9fb) | 3                      |
| [iden3-circuits](https://github.com/iden3/circuits)                  | `62b65d3cca3c07efc8269f8da56b21fa7dec650a` | [Trail of Bits 2024-05](https://github.com/trailofbits/publications/blob/master/reviews/2024-05-polygonlabs-iden3circuits-securityreview.pdf)                                                                                                           | [source](https://docs.privado.id/docs/verifier/circuits/)                         | 5                      |
| [nocturne](https://github.com/nocturne-xyz/protocol)                 | `f66fd0274e96f4eb62663552ecd29fb86e5b4a04` | [Zellic 2023-10](https://github.com/Zellic/publications/blob/master/Nocturne%20-%20Zellic%20Audit%20Report.pdf)                                                                                                                                         | [source](https://etherscan.io/address/0xA561492dFC1A90418Cc8b9577204d56C17CB32Ff) | 1                      |

<details>
<summary>All 25 circuits</summary>

| Unit                                                       | Main circuit                                                                                                                                                                                                                  | Constraints |
|------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------:|
| `tornado-core__withdraw`                                   | `circuits/withdraw.circom`                                                                                                                                                                                                    | 59,009      |
| `self__register-sha256-sha256-sha256-rsa-65537-4096`       | `circuits/circuits/register/instances/register_sha256_sha256_sha256_rsa_65537_4096.circom`                                                                                                                                    | 3,314,606   |
| `self__dsc-sha256-rsa-65537-4096`                          | `circuits/circuits/dsc/instances/dsc_sha256_rsa_65537_4096.circom`                                                                                                                                                            | 6,436,994   |
| `self__vc-and-disclose`                                    | `circuits/circuits/disclose/vc_and_disclose.circom`                                                                                                                                                                           | 225,194     |
| `semaphore__semaphore-v3-20`                               | `packages/circuits/semaphore.circom`                                                                                                                                                                                          | 17,689      |
| `circomlib__poseidon3`                                     | `test/circuits/poseidon3_test.circom`                                                                                                                                                                                         | 765         |
| `circomlib__eddsaposeidon`                                 | `test/circuits/eddsaposeidon_test.circom`                                                                                                                                                                                     | 21,246      |
| `circomlib__smtverifier10`                                 | `test/circuits/smtverifier10_test.circom`                                                                                                                                                                                     | 12,582      |
| `circomlib__lessthan`                                      | `test/circuits/lessthan.circom`                                                                                                                                                                                               | 36          |
| `circomlib__pedersen2`                                     | `test/circuits/pedersen2_test.circom`                                                                                                                                                                                         | 8,127       |
| `circomlib__babypbk`                                       | `test/circuits/babypbk_test.circom`                                                                                                                                                                                           | 10,114      |
| `maci__maci-polljoining-10`                                | `component main {public [nullifier, stateRoot, pollPublicKey, pollId]} = PollJoining(10);` (wrapper)                                                                                                                          | 23,926      |
| `maci__maci-messageprocessorqv-10-20-2`                    | `component main {public [totalSignups, index, batchEndIndex, currentSbCommitment, newSbCommitment, outputBatchHash, actualStateTreeDepth, coordinatorPublicKeyHash, voteOptions]} = MessageProcessorQv(10, 20, 2);` (wrapper) | 2,244,412   |
| `maci__maci-votetallyqv-10-1-2`                            | `component main {public [index, totalSignups, sbCommitment, currentTallyCommitment, newTallyCommitment]} = VoteTallyQv(10, 1, 2);` (wrapper)                                                                                  | 100,082     |
| `zk-email-verify__emailverifier`                           | `packages/circuits/tests/test-circuits/email-verifier-test.circom`                                                                                                                                                            | 5,993,156   |
| `zk-email-verify__rsaverifier65537-121-17`                 | `packages/circuits/tests/test-circuits/rsa-test.circom`                                                                                                                                                                       | 208,463     |
| `zk-email-verify__sha256bytes-640`                         | `packages/circuits/tests/test-circuits/sha-test.circom`                                                                                                                                                                       | 2,077,273   |
| `zk-email-verify__selectregexreveal-34-8`                  | `packages/circuits/tests/test-circuits/select-regex-reveal-test.circom`                                                                                                                                                       | 1,416       |
| `privacy-pools-core__withdraw`                             | `packages/circuits/circuits/main/withdraw.circom`                                                                                                                                                                             | 54,878      |
| `privacy-pools-core__commitment`                           | `packages/circuits/circuits/main/commitment.circom`                                                                                                                                                                           | 2,283       |
| `iden3-circuits__authv3-40-64`                             | `circuits/authV3.circom`                                                                                                                                                                                                      | 164,860     |
| `iden3-circuits__credentialatomicqueryv3offchain-40-32-64` | `circuits/credentialAtomicQueryV3.circom`                                                                                                                                                                                     | 196,801     |
| `iden3-circuits__linkedmultiquery-10-32-64`                | `circuits/linkedMultiQuery10.circom`                                                                                                                                                                                          | 644,027     |
| `nocturne__joinsplit`                                      | `packages/circuits/circuits/joinsplit.circom`                                                                                                                                                                                 | 124,892     |
| `nocturne__canonaddrsigcheck`                              | `packages/circuits/circuits/canonAddrSigCheck.circom`                                                                                                                                                                         | 35,226      |

</details>

<details>
<summary>Known unfixed audit findings (an alert on one of these counts as a real issue)</summary>

**tornado-core**

- ABDK-2 (Remaining Minor Issue): pathIndices should be explicitly bit-checked in Withdraw rather than inside the low-level Selector/DualMux (`circuits/merkleTree.circom:DualMux / circuits/withdraw.circom:Withdraw`)

**self**

- zkSec-2025-01 #02: Big Integer Zero-Check Is Not Sound (carry accumulation over native field) - client 'evaluating alternatives'; template unchanged in shape at pin (`circuits/circuits/utils/crypto/bigInt/bigIntComparators.circom:BigIntIsZero`)
- zkSec-2025-01 #05: Trusting the start offset of the public key inside the certificate may lead to signature forgery - only a heuristic mitigation (surrounding-byte check, PR #358), no DER parser (`circuits/circuits/dsc/dsc.circom (and register pubkey extraction)`)
- zkSec-2025-01 #06: The big integer library used for ECDSA verification is immature (`circuits/circuits/utils/crypto/bigInt/*`)
- zkSec-2025-01 #0e: Over-constraint in ECDSA for point duplication (forwarded to external library team) (`circuits/circuits/utils/crypto/signature/ecdsa/*`)
- zkSec-2025-01 #0f: Over-constraint in ECDSA for edge case in scalar multiplication (forwarded to external library team) (`circuits/circuits/utils/crypto/signature/ecdsa/*`)
- zkSec-2025-06 #07: The sparse Merkle tree stores truncated hashes instead of full hashes (collision risk) (`circuits/circuits/utils/crypto/merkle-trees/smt.circom`)
- zkSec-2025-09 #01: Invalid assumptions about Aadhaar name field formatting (nullifier/OFAC); only uppercase-normalisation mitigation (`circuits/circuits/register/register_aadhaar.circom, utils/aadhaar/*`)

**circomlib**

- V-CIRCOMLIB-VUL-001: Decoder accepting bogus output signal (critical, underconstrained) (`circuits/multiplexer.circom:Decoder (L78)`)
- V-CIRCOMLIB-VUL-002: Underconstrained points in Edwards2Montgomery (critical) (`circuits/montgomery.circom:Edwards2Montgomery (L30)`)
- V-CIRCOMLIB-VUL-003: Underconstrained points in Montgomery2Edwards (critical) (`circuits/montgomery.circom:Montgomery2Edwards (L49)`)
- V-CIRCOMLIB-VUL-004: Underconstrained points in MontgomeryAdd (critical) (`circuits/montgomery.circom:MontgomeryAdd (L89)`)
- V-CIRCOMLIB-VUL-005: Underconstrained points in MontgomeryDouble (critical) (`circuits/montgomery.circom:MontgomeryDouble (L122)`)
- V-CIRCOMLIB-VUL-006: Underconstrained outputs in BitElementMulAny (critical) (`circuits/escalarmulany.circom:BitElementMulAny (L34)`)
- V-CIRCOMLIB-VUL-007: Underconstrained outputs in Window4 (critical) (`circuits/pedersen.circom:Window4 (L25)`)
- V-CIRCOMLIB-VUL-008: Underconstrained outputs in WindowMulFix (critical) (`circuits/escalarmulfix.circom:WindowMulFix (L48)`)
- V-CIRCOMLIB-VUL-009: Underconstrained outputs in Bits2Point (warning: empty template) (`circuits/pointbits.circom:Bits2Point (L73)`)
- V-CIRCOMLIB-VUL-010: Underconstrained outputs in Point2Bits (warning: empty template) (`circuits/pointbits.circom:Point2Bits (L129)`)

**zk-email-verify**

- zkSecurity-07: Base64Decode does not distinguish between 'A' and '=' (padding char can replace 'A' with same output); client documented the behaviour instead of changing it (commit 27ccac) (`packages/circuits/lib/base64.circom:Base64Lookup/Base64Decode`)

**privacy-pools-core**

- Oxorio WARNING-2: Potential inclusion proof manipulation: actualDepth only range-checked (<= maxDepth), not enforced in the LeanIMT path computation (multiple valid proofs per leaf) (`packages/circuits/circuits/merkleTree.circom:LeanIMTInclusionProof`)
- Oxorio INFO-3: Value range checks performed after computing remainingValue (`packages/circuits/circuits/withdraw.circom:Withdraw`)
- Oxorio INFO-4: Use of non-anonymous components / `_ <==` discards (`packages/circuits/circuits/withdraw.circom:Withdraw`)

**iden3-circuits**

- TOB-IDEN3-3: Lack of domain separation in hash functions (`circuits/lib (claim/identity Poseidon hashing; e.g. lib/utils/claimUtils.circom, lib/utils/idUtils.circom)`)
- TOB-IDEN3-4: SpongeHash is not a sponge hash (`circuits/lib/utils/spongeHash.circom:SpongeHash`)
- TOB-IDEN3-5: Ambiguous padding in SpongeHash (`circuits/lib/utils/spongeHash.circom:SpongeHash`)
- TOB-IDEN3-6: Signature challenge does not bind claim or query (`circuits/auth/authV3.circom:AuthV3 (audited as authV2)`)
- TOB-IDEN3-7: Linked queries can prove expired or revoked claims (`circuits/linked/multiQuery.circom:LinkedMultiQuery`)

**nocturne**

- Zellic 3.5: Note encryption is unconstrained (note ciphertexts are free inputs, receiver may get an undecryptable/ mismatched note) (`packages/circuits/circuits/joinsplit.circom:JoinSplit`)

</details>

The 7 alerts triaged as real issues all match known unfixed findings:

| Unit                           | Tool   | `finding_index` | Alert                                                                     | Known finding       |
|--------------------------------|--------|----------------:|---------------------------------------------------------------------------|---------------------|
| `circomlib__babypbk`           | Civer  |               0 | Montgomery2Edwards does not satisfy weak safety                           | V-CIRCOMLIB-VUL-003 |
| `circomlib__babypbk`           | Civer  |               1 | Edwards2Montgomery does not satisfy weak safety                           | V-CIRCOMLIB-VUL-002 |
| `circomlib__babypbk`           | Civer  |               2 | MontgomeryAdd does not satisfy weak safety                                | V-CIRCOMLIB-VUL-004 |
| `circomlib__pedersen2`         | Civer  |               0 | MontgomeryAdd does not satisfy weak safety                                | V-CIRCOMLIB-VUL-004 |
| `circomlib__pedersen2`         | Civer  |               1 | Edwards2Montgomery does not satisfy weak safety                           | V-CIRCOMLIB-VUL-002 |
| `circomlib__pedersen2`         | Civer  |               2 | Montgomery2Edwards does not satisfy weak safety                           | V-CIRCOMLIB-VUL-003 |
| `privacy-pools-core__withdraw` | zkFuzz |               0 | Counterexample with `ASPTreeDepth` = p − 2, which passes the depth check  | Oxorio WARNING-2    |

## Result Files

All paths inside raw tool output are paths inside the zkhydra Docker container (e.g. `/evaluation_tool/...` or `/zkhydra/...`).

### Main experiment (`results/tp/`)

```text
results/tp/
├── summary.json             # zkhydra's run summary for both modes
├── isolated/                # isolated mode (zkhydra: --zkbugs-mode direct, folder direct/)
│   ├── summary.json         # per-bug run status of every tool
│   └── <bug>/
│       ├── ground_truth.json    # the dataset annotation: vulnerability, root cause, location, source
│       ├── run.log              # zkhydra's log (only for bugs that were re-run)
│       └── <tool>/
│           ├── raw.txt          # the tool's raw stdout/stderr
│           ├── parsed.json      # tool-specific parsed output
│           ├── results.json     # findings in zkhydra's unified format
│           ├── tool_output.json # status, return code, and output (ConsCS only)
│           └── evaluation.json  # the verdict against the ground truth
└── project/                 # project mode (zkhydra: --zkbugs-mode original, folder original/), same layout
```

`<tool>` is one of `picus`, `circom_civer`, `circomspect`, `zkfuzz`, and `conscs`.
A tool folder without `results.json` means the run ended in an error or a timeout (see `raw.txt` and `summary.json`).
The converse does not hold: some failed runs still have a `results.json` and an `evaluation.json` with `FalseNegative`.
Figures and tables therefore take error and timeout from `raw.txt` (`scripts/tools_evaluation.py`), and `data/tools-evaluation.json` holds the final label of every run.
The main [README](../README.md#main-experiment-known-vulnerabilities) (*Setup*) lists the errors caused by the setup rather than the tools.
Some `run.log` files come from re-runs that also ran Ecne, which is not part of the evaluation; they are kept unchanged as raw logs.

`evaluation.json` has the following fields:

| Field                       | Meaning                                                                                                     |
|-----------------------------|-------------------------------------------------------------------------------------------------------------|
| `status`                    | `TruePositive` (the tool detected the bug) or `FalseNegative` (it did not).                                 |
| `reason`                    | zkhydra's explanation of the automatic comparison with the ground truth.                                    |
| `need_manual_analysis`      | `true` if the automatic comparison could not decide, e.g. because the tool's output has no source location. |
| `manual_analysis`           | `N/A` if zkhydra decided automatically; `Done` if the authors decided the `status` manually.                |
| `manual_analysis_reasoning` | Unused (empty or `N/A`).                                                                                    |

### False-positive experiment (`results/fp/`)

```text
results/fp/
├── summary.json             # zkhydra's run summary (per circuit and tool)
└── <project>__<circuit>/
    ├── fp_candidates.json   # per tool: run status, soundness alerts, lint warnings, tool errors
    └── <tool>/
        ├── raw.txt, parsed.json, results.json, tool_output.json
        └── fp_triage.json   # the authors' verdict per soundness alert (only if the tool raised one)
```

In `fp_candidates.json`, each tool's `status` is `success`, `timeout`, or a failure.
Its `soundness` list holds the soundness alerts (under-constrained, over-constrained, and computational findings), which are the candidate false positives.
Its `warnings` list holds Circomspect's lint warnings, which count only as review burden.
`fp_triage.json` lists one entry per soundness alert: `finding_index` (its position in `soundness`), `finding_fp` (a fingerprint of the finding, so a verdict cannot attach to a different alert after a re-run), and `status` (`FalsePositive`, `RealIssue`, or `Undecided`).

## Expected Numbers

A correct reproduction of the figures and tables gives these numbers.

**Main experiment, isolated mode (70 bugs):**

| Tool        | TP | FN | Error | Timeout |
|-------------|---:|---:|------:|--------:|
| Picus       | 10 | 41 |     0 |      19 |
| Civer       | 12 | 18 |    26 |      14 |
| Circomspect |  0 | 57 |    13 |       0 |
| zkFuzz      | 25 | 16 |     4 |      25 |
| ConsCS      | 11 | 43 |     5 |      11 |

58 true positives in total; at least one tool detects 27 of the 70 bugs.

**Main experiment, project mode (56 bugs):**

| Tool        | TP | FN | Error | Timeout |
|-------------|---:|---:|------:|--------:|
| Picus       |  0 | 30 |    20 |       6 |
| Civer       |  1 |  8 |    36 |      11 |
| Circomspect |  1 | 54 |     1 |       0 |
| zkFuzz      |  4 | 12 |     4 |      36 |
| ConsCS      |  1 | 21 |     9 |      25 |

7 true positives in total; at least one tool detects 6 of the 56 bugs.

**False-positive experiment (25 circuits; Figure 3 shows Done split into FP and No FP, Error, and Timeout):**

| Tool        | Done | Timeout | Error | Alerts | FP | Real | Circuits with ≥1 FP |
|-------------|-----:|--------:|------:|-------:|---:|-----:|--------------------:|
| Picus       | 14   | 11      | 0     | 0      | 0  | 0    | 0/14                |
| Civer       | 9    | 11      | 5     | 12     | 6  | 6    | 2/9                 |
| Circomspect | 24   | 0       | 1     | 6      | 6  | 0    | 3/24                |
| zkFuzz      | 7    | 18      | 0     | 2      | 1  | 1    | 1/7                 |
| ConsCS      | 12   | 11      | 2     | 0      | 0  | 0    | 0/12                |
| **Total**   | 66   | 51      | 8     | 20     | 13 | 7    |                     |

Circomspect additionally raises 28 lint warnings.
