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
| P1-C1 | Valid mapped decompositions preserve exact links from interpretation nodes to originating base-graph structures, enabling a reported discrimination witness to be localized. | Formal mapping definitions and constructor tests establish preservation; E01 additionally measures overlap between mapped witnesses and frozen synthetic interventions. | `specification/formalism.md`; package mapping tests; `fig01-structural-views.pdf`; `fig03-composition-transitions.pdf`. | Introduction; Sections 3, 5, and 6; formal appendix. | Proposed |
| P1-C2 | Unary and multi-input operators are closed over valid Abstract Graphs by construction. | Typed semantics and package contract tests establish well-formedness. This is a formal construction, not an empirical novelty claim. | `specification/operator-inventory.md`; package contract tests. | Sections 3--4; formal appendix. | Proposed |
| P1-C3 | Under a declared attributed-subgraph equivalence, structurally equivalent mapped components receive stable canonical certificates and configured feature identities. | Frozen equivalence and identity specification; package stability tests; controlled collision analysis by hash width; explicit separation of certificate equality from bounded-hash equality. | Identity specification; package tests; E01 collision analysis. | Introduction contribution 3; Sections 3--4; Results: RQ1. | Proposed |
| P1-C4 | Admissible deterministic operator programs are equivariant to permitted base-node relabelling, up to Abstract Graph representation equivalence. | Equivariance included in the admissible-operator definition; property tests over the normative reference operators; user-defined callbacks outside this contract explicitly excluded. | Formal operator contract; package permutation tests. | Section 4; formal appendix; reproducibility statement. | Proposed |
| P1-C5 | Predeclared operator expressions induce factor-specific, potentially incomparable discrimination profiles with measurable runtime, memory, and representation-size costs. | Frozen expression and pair suites; held-out generator settings; E01 factor-specific discrimination; E02 matched-cost measurements with repeated-run uncertainty and failure boundaries. | `fig02-discrimination-atlas.pdf`; `fig04-pareto-frontiers.pdf`; `tab02-expression-tradeoffs.tex`. | Introduction; Sections 5--7. | Proposed |
| P1-C6 | Additive union agrees with lossless concatenation under matched identities, while ordered and relational programs can create distinctions absent from atomic union by constructing new mapped objects or relations. | Compare atoms, lossless concatenation, an equally informed flat relational materialization, and graph-valued composition. Require additive parity; test held-out gains over concatenation; require agreement with the flat control at matched information and compare localization and cost. | `fig03-composition-transitions.pdf`; `fig04-pareto-frontiers.pdf`; E01/E02 raw results. | Abstract; Introduction; RQ1--RQ2; Results; Discussion. | Proposed |
| P1-C7 | The AG language has a documented coverage boundary across vertex/edge histograms, shortest-path, graphlet, WL subtree, and NSPDK features: each construction is classified as faithful, a named bounded proxy, or unsupported. | Specify the required feature identity and multiplicity for every family. Independent parity checks support every faithful designation; failed candidates and missing primitives remain explicit negative results. | `tab01-baseline-expressions.tex`; E01 parity results. | Introduction; Sections 2 and 4--6. | Proposed |

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
| P1-C6 | P1-C1, P1-C2, P1-C5 | A compositional change must be mapped, well-formed, and compared with equally informed controls at matched cost. |
| P1-C7 | P1-C2, P1-C3 | Coverage classifications require valid programs and matched identity semantics. |

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
