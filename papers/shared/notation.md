# Shared notation and invariants

This guide defines the mathematical vocabulary used throughout the
AbstractGraph paper programme. Paper-specific specifications may restrict these
objects further, but must not silently change their meaning. The implementation
status of each Paper 1 concept is recorded in
[`../paper-01-representation/specification/implementation-inventory.md`](../paper-01-representation/specification/implementation-inventory.md).

## Conventions

- Graphs are finite.
- Upper-case letters denote graphs, sets, or structured objects; lower-case
  letters denote elements or functions.
- A prime denotes an output or successor state, as in \(A'\).
- Equality \(=\) means literal equality under the declared data model.
  Equivalence \(\equiv\) means equality up to a declared relation such as graph
  isomorphism or identifier relabelling.
- Node identifiers are implementation handles unless a paper explicitly makes
  them semantic attributes.
- `Base graph`, `interpretation graph`, `mapped subgraph`, `operator program`,
  `structural feature identity`, and `provenance` have the meanings defined in
  [`terminology.md`](terminology.md).

## Core objects

### Base graph

An attributed base graph is

\[
G=(V,E,X_V,X_E,\tau_G),
\]

where \(V\) and \(E\) are its node and edge sets, \(X_V\) and \(X_E\) are
node- and edge-attribute maps, and \(\tau_G\) records the graph kind, including
directedness. A paper must state its supported graph kinds and attribute
equivalence rules. Paper 1 currently targets finite simple directed and
undirected graphs; multigraphs and hypergraphs are outside its implementation
scope.

For \(U\subseteq V\) and \(F\subseteq E\), write

\[
G[U]=(U,E\cap(U\times U))
\]

for a node-induced subgraph and \(G\langle F\rangle\) for an edge-induced
subgraph containing the endpoints of \(F\). Attribute maps are restricted to
the selected nodes and edges unless an operator contract says otherwise.

### Mapped-subgraph space

Let \(\mathcal{S}(G)\) be the mapped-subgraph space permitted by a paper's data
model. Each \(s\in\mathcal{S}(G)\) is represented by

\[
s=(V_s,E_s,X_V|_{V_s},X_E|_{E_s}),
\qquad V_s\subseteq V,\quad E_s\subseteq E.
\]

Node-induced and edge-induced mapped subgraphs are both permitted when the
producing operator declares which materialisation rule it uses. Mapped
subgraphs may overlap, may equal the whole base graph, and need not be
connected. Empty mapped subgraphs are permitted only when an operator contract
explicitly includes them; reference decomposition operators should suppress
them by default.

### Interpretation graph and mapping

An interpretation graph is

\[
I=(V_I,E_I,X_I,R_I),
\]

where each interpretation node denotes a mapped subgraph, \(X_I\) contains
derived node attributes such as identities or summaries, and \(R_I\) gives the
declared semantics of interpretation edges. Interpretation edges are not
assumed to mean adjacency: a relation may encode overlap, derivation,
compatibility, or another named relation.

The mapping

\[
\mu:V_I\rightarrow\mathcal{S}(G)
\]

associates every interpretation node with exactly one mapped subgraph. The
mapping need not be injective: distinct interpretation nodes may map to the
same base subgraph when their derivations, roles, or interpretation attributes
differ. It need not cover all of \(G\) unless an operator contract requires
coverage.

### Abstract Graph representation

The semantic representation is

\[
A=(G,I,\mu).
\]

Label, attribute, and interpretation-edge functions used to construct or update
\(A\) belong to the execution configuration rather than to the semantic tuple.
When such configuration matters, write

\[
\Gamma=(\ell,a,r,\theta),
\]

where \(\ell\) assigns interpretation-node labels or identities, \(a\)
computes derived attributes, \(r\) constructs interpretation relations, and
\(\theta\) contains their parameters. An implementation state may therefore be
written \((A,\Gamma)\) without redefining the Abstract Graph itself.

## Equivalence and identity

### Permitted relabelling

A permitted base-node relabelling is a bijection \(\rho:V\to V'\) that
preserves graph kind, adjacency or arc direction, and all attributes declared
semantic by the experiment. It induces a relabelled base graph \(\rho(G)\) and
mapped subgraph \(\rho(s)\).

Two attributed subgraphs are structurally equivalent under an experiment's
declared attribute projection \(q\), written

\[
s_1\equiv_q s_2,
\]

when there exists an isomorphism preserving directedness and the projected
node and edge attributes. Paper 1 must declare \(q\) for every identity
experiment. The current implementation's graph identity projection uses the
attribute named `label` and ignores other attributes.

### Canonical certificate and feature identity

Keep the following layers distinct:

\[
c_q(s) \quad\text{canonical certificate},
\]

\[
h_b(c_q(s)) \quad\text{bounded hash at width }b,
\]

and

\[
\phi_{q,b}(s)=h_b(c_q(s)) \quad\text{structural feature identity}.
\]

The intended certificate satisfies

\[
s_1\equiv_q s_2 \Longrightarrow c_q(s_1)=c_q(s_2).
\]

Whether the converse holds must be stated for the selected canonicalisation
method. A bounded feature identity is not a proof of structural equivalence:
different certificates may collide after hashing. Every experiment using
\(\phi_{q,b}\) must record \(q\), \(b\), the canonicalisation and hash
algorithms, and its collision policy.

## Provenance

For a derived object \(y\), define base-graph provenance as

\[
\pi_G(y)=(V_y,E_y),
\qquad V_y\subseteq V,\quad E_y\subseteq E.
\]

For an interpretation node \(u\), its extensional provenance is exactly its
mapping:

\[
\pi_G(u)=(V_{\mu(u)},E_{\mu(u)}).
\]

Derivation provenance records how the object was produced:

\[
\delta(y)=(o,\theta,Y_{\mathrm{parent}}),
\]

where \(o\) is the producing operator, \(\theta\) is its serialized parameter
state, and \(Y_{\mathrm{parent}}\) is the ordered or unordered parent collection
declared by the operator contract. Extensional provenance \(\pi_G\) and
derivation provenance \(\delta\) are complementary and must not be conflated.

Provenance is not attribution. Provenance identifies origins exactly;
attribution assigns model-derived relevance and may be uncertain or unstable.

## Operators and programs

An operator of arity (k) is a partial, typed function

\[
o:\prod_{j=1}^{k}\mathcal{A}_{C_{\mathrm{in},j}}\rightharpoonup
  \mathcal{A}_{C_{\mathrm{out}}},
\]

where \(\mathcal{A}_{C}\) is the set of valid Abstract Graphs satisfying
contract \(C\). A contract declares:

- accepted graph kinds and required attributes;
- which of \(G\), \(I\), and \(\mu\) may be read or changed;
- mapped-subgraph materialisation and coverage behavior;
- determinism and random-state requirements;
- interpretation-edge semantics;
- provenance behavior;
- failure conditions; and
- time and memory complexity.

Thus the operator family is closed over valid Abstract Graphs: whenever the
input contracts hold, an operator returns another Abstract Graph. For
compatible unary operators, sequential composition is

\[
P=o_k\circ\cdots\circ o_1,
\qquad
P(A)=o_k(\cdots o_2(o_1(A))\cdots).
\]

Compatibility requires the output contract of \(o_i\) to imply the input
contract of \(o_{i+1}\). `Operator program` includes sequential, additive,
parallel/product, conditional, and bounded iterative composition when their
semantics are declared. A serialized operator program is written
\(\sigma_P(P)\). Closure guarantees composability and well-formed outputs; it
does not imply that an operator refines its input or monotonically increases
discrimination.

## Representation equivalence

Two Abstract Graph representations \(A=(G,I,\mu)\) and
\(A'=(G',I',\mu')\) are equivalent under \((q,R_I)\), written

\[
A\equiv_{q,R_I}A',
\]

when there are graph isomorphisms \(\rho:G\to G'\) and \(\eta:I\to I'\) that
preserve the attributes selected by \(q\), preserve declared interpretation
relations \(R_I\), and make the mapping commute:

\[
\rho(\mu(u))=\mu'(\eta(u))
\quad\text{for every }u\in V_I.
\]

This is the comparison relation used for permutation and serialization tests;
literal NetworkX node order is not semantic.

## Required invariants

An Abstract Graph or operator program used as Paper 1 evidence must satisfy:

1. **Mapping validity:** every node and edge in every \(\mu(u)\) belongs to
   \(G\), with matching semantic attributes.
2. **Interpretation totality:** \(\mu(u)\) is defined for every \(u\in V_I\).
3. **Provenance completeness:** \(\pi_G(y)\) contains all and only the base
   nodes and edges required by the declared semantics of \(y\), and
   \(\delta(y)\) identifies its derivation when required.
4. **Permutation invariance:** for permitted \(\rho\) and deterministic \(P\),
   \(P(\rho(A))\equiv_{q,R_I}\rho(P(A))\).
5. **Determinism:** fixed input, configuration, program, software version, and
   random state produce equivalent outputs and identities.
6. **Composition closure:** every adjacent pair in a valid program has
   compatible contracts, and every successful output satisfies the declared
   output contract.
7. **Identity consistency:** \(s_1\equiv_q s_2\) implies equal canonical
   certificates and feature identities under the same identity configuration.
8. **Serialization round trip:** for each supported serializer \(\sigma\) and
   deserializer \(\sigma^{-1}\),
   \(\sigma^{-1}(\sigma(z))\equiv z\) under the declared equivalence for
   programs or representation states.

## Cross-paper task boundaries

| Result type | Object returned | Scientific question |
| --- | --- | --- |
| Representation | \(A\), \(P(A)\), \(\phi(s)\), or provenance | What structure is represented and retained? |
| Prediction | \(\hat y=f(A)\) | What target can be inferred from the representation? |
| Attribution or explanation | relevance \(\alpha(y,\hat y)\) plus provenance | Which represented objects influence a prediction, and how faithfully? |
| Feasibility decision | score or decision \(F(A)\) | Is a complete or partial structure admissible? |
| Constructive action | \(A' = c(A)\) plus a trace | What structural edit or extension is performed? |

Paper 1 reports representation results only. Later papers may reuse Paper 1
objects but must not present predictive accuracy, attribution quality,
feasibility, or construction as evidence for a representation invariant.

## Paper 1 decisions still to freeze

- The normative canonical-certificate algorithm and whether it is complete for
  the supported graph class.
- The bounded-hash width or widths and collision detection/resolution policy.
- The normalized on-disk schemas for Abstract Graph state and provenance.
- The normative reference-operator subset and each operator's typed contract.
- Exact failure/error categories and validation API.

These are tracked in
[`../paper-01-representation/specification/formalism.md`](../paper-01-representation/specification/formalism.md)
and do not change the shared meaning of the notation above.
