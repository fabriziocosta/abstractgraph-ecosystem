# Abstract Graphs: A Compositional Representation of Graph Structure

## Abstract

To be drafted after the central claims and primary results are frozen.

## 1. Introduction

- Graph feature extraction commonly discards the explicit relationship between
  derived structural components and the original graph.
- Abstract Graphs retain mapped subgraphs as first-class objects.
- The paper tests whether graph-valued composition adds anything beyond atomic
  extraction and lossless feature concatenation.
- Mapped witnesses must localize the structural intervention responsible for a
  distinction.
- State the contributions using claim IDs P1-C1 through P1-C7.

## 2. Related work

- Graphlets and motif counting
- Weisfeiler-Lehman representations
- Graph decompositions and hierarchical graph representations
- Graph grammars and compositional graph languages
- Provenance and traceability in graph feature systems

## 3. Abstract Graph formalism

- Base graph and attribute model
- Interpretation graph
- Mapping to base-graph subgraphs
- Structural identities and equivalence
- Provenance

## 4. Operator programs

- Operator contracts and typing
- Composition
- Representation invariants and admissibility
- Multiplicity, deduplication, and ordering semantics
- Reference operator suite
- Complexity analysis

## 5. Experimental protocol

- Research questions and hypotheses
- Synthetic and real graph families
- Independently validated baseline translations
- Atomic, lossless-concatenation, and graph-composition controls
- Frozen expression suite and held-out generator settings
- Metrics and statistical protocol
- Compute and reproducibility controls

## 6. Results

- RQ1: baseline parity and intrinsic structural discrimination
- RQ1: composition versus atomic and concatenated controls
- RQ1: mapped-witness localization
- RQ1: predictive accessibility, pooling, and hash-width ablations
- RQ1: comparison with adjacent representations
- RQ2: runtime, memory, and representation-size costs
- RQ2: factor-specific Pareto frontiers and failure boundaries

## 7. Discussion

- What explicit mapped structure enables
- Limits of equivalence and canonicalisation choices
- Scaling boundaries
- Threats to validity
- Scope intentionally deferred to later papers

## 8. Conclusion

## Reproducibility statement
