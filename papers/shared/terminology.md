# Canonical Terminology

| Preferred term | Definition | Avoid unless distinct |
| --- | --- | --- |
| Base graph | The original attributed graph. | source graph, raw graph |
| Interpretation graph | A graph whose nodes represent mapped subgraphs. | abstract graph when referring only to this component |
| Mapped subgraph | A structural component tied to a region of the base graph. | motif node, component node |
| Operator | A composable transformation or decomposition. | transform, step |
| Operator program | A sequence or composition of operators. | pipeline when formal composition is intended |
| Structural feature identity | The canonical or hashed identity of a mapped component. | feature hash when the scheme need not be hashing |
| Provenance | The exact mapping from a derived object to originating base-graph nodes and edges. | explanation |
| Feasibility model | A model of admissible graph structure. | validity model unless validity is formally defined |
| Constructive operator | An operation that adds, removes, replaces, or joins components. | edit without specifying its semantics |
| Repair trace | An interpretable sequence transforming an input graph into a feasible graph. | generation trace |

## Usage rules

1. Provenance is a representation property; attribution is a model-derived
   relevance score. Exact provenance does not imply a faithful explanation.
2. Use “interpretation node” for a node of the interpretation graph. Do not
   substitute “abstract node,” “motif node,” or “component node” without an
   explicit definition.
3. State whether “identity” is canonical, hash-based, or both.
4. State whether an operator acts on the base graph, interpretation graph,
   mapping, or a combination of them.
