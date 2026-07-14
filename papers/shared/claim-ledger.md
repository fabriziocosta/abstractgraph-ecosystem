# Programme claim ledger

This ledger is the authoritative index of manuscript claims and their evidence.
Claim IDs are stable even if wording is revised. A claim may appear in a
manuscript only at or below the strength supported by its status and linked
artifacts.

## Status rules

| Status | Entry requirement |
| --- | --- |
| `Proposed` | Scientific claim and intended evidence are identified. |
| `Specified` | Terms, scope, hypotheses, metrics, and acceptance criteria are frozen. |
| `Pilot-supported` | Versioned pilot evidence supports the claim without constituting the final confirmatory result. |
| `Confirmed` | Frozen confirmatory evidence and reproducible artifacts satisfy the predeclared criteria. |
| `Rejected` | Evidence contradicts the claim or fails its acceptance criteria. |
| `Revised` | Scope or wording changed materially; the entry links the reason and replacement claim where applicable. |

Documentation or implementation alone may support specification, but cannot
confirm an empirical claim. Negative and boundary results remain linked to the
claim they constrain.

## Paper 1 claims

| Claim ID | Claim | Planned evidence and acceptance target | Planned artifact | Manuscript location | Status |
| --- | --- | --- | --- | --- | --- |
| P1-C1 | Valid mapped decompositions preserve exact links from every interpretation node to the originating base-graph nodes and edges. | Formal mapping/provenance definitions; validator and reference-operator property tests showing mapping validity and complete extensional provenance; full-state round trips equivalent under the declared relation. | `specification/formalism.md`; E00 validation results; mapping/provenance test report; serialization table. | Introduction contribution 1; Section 3; Results: representation validation. | Proposed |
| P1-C2 | Unary and multi-input operators form a composable family closed over valid Abstract Graphs while preserving their declared representation contracts. | Typed operator semantics and closure argument; contract table for the normative operator suite; composition and behavioral XML round-trip tests; custom-decomposition constructor tests; discrimination comparison in E01. | `specification/operator-inventory.md`; E00 and E01 results; operator-contract table. | Introduction contribution 2; Section 4; Results: structural discrimination. | Proposed |
| P1-C3 | Under a declared attributed-subgraph equivalence, structurally equivalent mapped components receive stable canonical certificates and configured feature identities. | Frozen equivalence and identity specification; cross-run/process/platform stability tests; controlled collision analysis by hash width; explicit separation of certificate equality from bounded-hash equality. | Identity specification; E00 stability and E01 collision results; identity table/figure. | Introduction contribution 3; Sections 3--4; Results: validation and RQ1. | Proposed |
| P1-C4 | Deterministic reference operator programs are invariant to permitted base-node relabelling, up to Abstract Graph representation equivalence. | Generated permutation tests across graph families, attribute-order perturbations, and program depths; equivalent interpretation graphs and commuting mappings for all deterministic reference programs; exclusions reported for stochastic operators. | E00 validation results; permutation test report; invariance table. | Introduction contribution 4; Section 5; Results: representation validation. | Proposed |
| P1-C5 | The discrimination and computational cost of the reference representation are characterized over graph size, density, attributes, and operator-program depth. | E01 comparisons with frozen adjacent representations; E02 runtime and peak-memory measurements; local complexity table; repeated-run uncertainty and documented failure boundaries. | E01/E02 raw results; complexity table; discrimination and scaling figures. | Introduction contribution 5; Sections 4--6; Discussion: scaling boundaries. | Proposed |

Paths in the table are relative to `papers/paper-01-representation/` unless
otherwise stated. Experiment family IDs refer to
[`../paper-01-representation/experiments/manifest.yaml`](../paper-01-representation/experiments/manifest.yaml).

## Claim dependencies

| Claim | Depends on | Reason |
| --- | --- | --- |
| P1-C1 | None | Mapping and provenance are foundational representation properties. |
| P1-C2 | P1-C1 | Composition must preserve valid mappings and declared provenance. |
| P1-C3 | P1-C1 | Identities are assigned to valid mapped subgraphs. |
| P1-C4 | P1-C2, P1-C3 | The invariance claim compares operator outputs and their identities. |
| P1-C5 | P1-C2 | Expressiveness and scaling are properties of declared operator programs. |

## Evidence update protocol

For every status change:

1. record the exact code revision and dirty-worktree state;
2. link immutable raw result IDs rather than only derived figures;
3. name the frozen configuration, dataset version, seeds, and environment;
4. link the manuscript table, figure, or theorem supported by the evidence;
5. record counterevidence and boundary conditions; and
6. update the decision log in `papers/PLAN.md` for any material claim revision.

The implementation audit is informative context, not claim evidence:
[`../paper-01-representation/specification/implementation-inventory.md`](../paper-01-representation/specification/implementation-inventory.md).
