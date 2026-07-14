# Shared Notation and Invariants

This is the working notation specification for the paper series. Paper 1 must
validate it against the implementation before it is treated as final.

## Objects

| Symbol | Meaning |
| --- | --- |
| \(G=(V,E,X_V,X_E)\) | Attributed base graph with node and edge attributes. |
| \(I=(V_I,E_I)\) | Interpretation graph. |
| \(\mu:V_I\to\mathcal{S}(G)\) | Mapping from interpretation nodes to subgraphs of \(G\). |
| \(A=(G,I,\mu)\) | Working Abstract Graph representation. |
| \(o:A\to A'\) | Operator acting on an Abstract Graph representation. |
| \(P=o_k\circ\cdots\circ o_1\) | Operator program. |
| \(\phi(s)\) | Structural feature identity of mapped subgraph \(s\). |
| \(\pi(y)\) | Provenance of derived object \(y\) in the base graph. |

`\mathcal{S}(G)` denotes the permitted mapped-subgraph space. The exact rules
for induced versus non-induced subgraphs, empty mappings, overlaps, and
attribute preservation remain Paper 1 specification decisions.

## Candidate representation invariants

- **Mapping validity:** every node and edge referenced by \(\mu(v)\) exists in
  the associated base graph.
- **Provenance completeness:** every derived component records all originating
  base-graph nodes and edges required by its semantics.
- **Permutation invariance:** relabelling base-graph node identifiers does not
  change decomposition structure or structural identities, up to isomorphism.
- **Determinism:** a deterministic operator program and identical attributed
  input produce equivalent output and identity assignments.
- **Composition closure:** the output of each composable operator satisfies the
  input contract of its successor.
- **Serialization round-trip:** supported serialized representations preserve
  graph structure, mappings, attributes, identities, and provenance.
- **Identity consistency:** structurally equivalent mapped components receive
  equal identities under the declared equivalence relation.

## Open decisions for Paper 1

- [ ] Directed graph, multigraph, self-loop, and hypergraph scope.
- [ ] Node and edge attribute equivalence rules.
- [ ] Whether interpretation edges have formal relation types.
- [ ] Permitted overlap between mapped subgraphs.
- [ ] Empty, disconnected, and whole-graph mapped components.
- [ ] Canonicalisation algorithm and hash collision policy.
- [ ] Operator typing and error semantics.
