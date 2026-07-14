# Paper 1 — Abstract Graph Representation

Working title: **Abstract Graphs: A Compositional Representation of Graph
Structure**

## Central question

How can meaningful subgraphs be represented as first-class objects while
remaining linked to the original graph?

## Central claim

Explicit mapped decompositions form a reproducible, compositional, traceable,
and computationally usable representation of graph structure.

## Scope

This paper covers `abstractgraph` only. Predictive performance, learned
explanations, feasibility, and generation are out of scope except where needed
to motivate later work.

## Directory layout

- `manuscript/`: outline and manuscript source.
- `specification/`: definitions, invariants, operator contracts, and open
  formal decisions.
- `experiments/`: experiment manifests and configurations.
- `analysis/`: analysis plans and scripts added during implementation.
- `results/`: immutable raw-result policy and result indexes; do not hand-edit
  generated results.
- `figures/`: figure specifications and generated figure index.
- `tables/`: table specifications and generated table index.
- `reproducibility/`: code revision, environment, and checklist records.

Shared terminology, notation, datasets, benchmarks, and references live in
[`../shared`](../shared/README.md).

## Completion gate

The paper is ready for submission when definitions match implementation,
identities and provenance pass their declared tests, scaling limits are
reported, comparisons are fair, and every central claim links to evidence in
the shared claim ledger.
