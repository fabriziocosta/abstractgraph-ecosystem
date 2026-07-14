# Paper 1 — A closed operator algebra for programmable graph representations

Working title:

> **Abstract Graphs: A Closed Operator Algebra for Programmable Structural Representations**

Alternative, more conservative title:

> **Abstract Graphs: A Compositional Representation of Graph Structure**

## Paper in one paragraph

An Abstract Graph (AG) couples a base graph with an interpretation graph whose
nodes refer back to structures in the base graph. The central construction is a
many-operator algebra closed over this representation: unary and multi-input
operators consume AGs and produce AGs, so their expressions can be composed
without leaving the common representational space. The operators may identify
nodes, edges, neighborhoods, paths, cycles, graphlets, or relations between
such objects. Composition modifies the representation; it is not intrinsically
a refinement and carries no general promise of monotone discrimination. We
instead measure which graph pairs each expression distinguishes or collapses,
which distinctions are accessible to simple predictive probes, and what
runtime, memory, and representation size it requires. Established methods such
as path features, Weisfeiler--Lehman refinement, and NSPDK become particular
expressions in the same algebra rather than conceptually unrelated baselines.

## Central scientific question

> Which graph transformations can be expressed by a closed algebra of Abstract
> Graph operators, how do different expressions change discrimination, and what
> computational costs do those choices incur?

This question has three parts:

1. **Resolution:** which controlled structural changes alter the representation?
2. **Accessibility:** are those changes directly recoverable from the feature
   space by a simple model?
3. **Cost:** what runtime, memory, and representation size are required?

## Central claim

> **Abstract Graphs form a common, closed representational space for a
> composable family of structural operators. This makes graph representations
> programmable and extensible, while the discrimination and computational cost
> of each expression remain empirical, measurable properties.**

Here, expressive means that many structural transformations can be stated and
combined in one language. It does not mean that composition follows an ordered
refinement process, that a longer expression discriminates more graphs, or that
Abstract Graphs distinguish every pair of non-isomorphic graphs. Operators
simply transform AGs. Any refinement, preservation, or collapse observed after
vectorization is a property of a particular expression and experiment.

Mapped subgraphs and provenance are essential supporting properties. They let
the study identify not only whether two graphs differ under a program, but
which concrete structural components caused the difference.

## Formal view: a closed multi-operator algebra

At implementation level, write an Abstract Graph as

\[
A=(G,I),
\]

where \(G\) is the base graph and \(I\) is the interpretation graph. Each node
of \(I\) carries the base-graph structure it denotes through its
`mapped_subgraph` payload. Equivalently, the semantics may be unpacked as
\((G,I,\mu)\), with \(\mu\) making that mapping explicit.

Let \(\mathcal{AG}\) denote the space of valid Abstract Graphs and let
\(\Omega\) be a signature containing unary and multi-input operators. An
operator of arity \(k\) has the form

\[
\omega: \mathcal{AG}^{k} \to \mathcal{AG}.
\]

Every operator returns a valid AG by construction. Operator expressions are
terms generated from \(\Omega\); sequential composition, addition, products,
branches, and iteration are expression constructors rather than exits into
incompatible intermediate representations.

This closure is the primary formal property. There is no universal order
\(A\preceq\omega(A)\): an operator may add, remove, aggregate, relate, or replace
interpreted structures. Consequently, compositionality establishes
well-formedness and expressivity, not refinement or monotonicity.

## Experimental view: expressions induce partitions of graph space

Let \(P\) be an operator program and let \(\Sigma_P(G)\) be its deterministic
representation signature. Define

\[
G\equiv_P H
\quad\Longleftrightarrow\quad
\Sigma_P(G)=\Sigma_P(H).
\]

If \(G\equiv_P H\), the program collapses the pair. Otherwise it discriminates
the pair. The equivalence classes induced by \(P\) form a partition of the
evaluated graph space.

For any two expressions---including an additive extension

\[
P_{+}=P_1\oplus P_2,
\]

whether one partition refines another is determined from their resulting
signatures. Losslessly retaining both branch signatures is one sufficient
condition for an additive expression to preserve the distinctions of \(P_1\),
but this is a feature-encoding fact, not a general law of the AG algebra.

## A minimal extension interface

The algebra is intended to be easy to extend. A domain expert can write a
Python callback that accepts a NetworkX graph and returns a concrete list of
node groups:

```python
def decompose(graph: nx.Graph) -> list[list[Hashable]]:
    ...
```

The groups form a partition when they are disjoint and exhaustive; operators
may also deliberately return a cover with overlap or omit nodes when their
contract permits it. A library constructor wraps this callback as an
\(\mathcal{AG}\to\mathcal{AG}\) operator: it applies the decomposition to the
appropriate mapped graph, materializes the induced subgraphs, and records the
mapping and provenance required by downstream operators. Analogous constructors
support edge decompositions and global transformations.

This narrow interface lowers the cost of encoding domain knowledge. It also
makes ad hoc operator generation by an LLM technically plausible: generated
code need only satisfy a small input/output contract to participate in the
larger algebra. Such code must still be validated for determinism, coverage,
invariance, resource use, and semantic correctness before use.

## Representation pipeline

The complete experimental pipeline is

\[
G
\xrightarrow{P}
A_P(G)
\xrightarrow{v_b}
x_{P,b}(G)
\xrightarrow{f}
\widehat y,
\]

where:

- \(P\) is a serialized operator expression;
- \(A_P(G)\) is the resulting Abstract Graph;
- \(v_b\) converts mapped components and relations into a sparse feature vector
  at identity width \(b\); and
- \(f\) is a deliberately simple diagnostic classifier or regressor.

### Node-level and graph-level representations

The native vectorization is node-level. For base node \(v\) and structural
feature bucket \(j\), define

\[
Z_{P,b}(G)_{v,j}=
\sum_{u\in V_I}
\mathbf 1[v\in V_{\mu(u)}]
\mathbf 1[\phi_b(\mu(u))=j]a(u),
\]

where \(a(u)\) is the scalar or vector contribution assigned to interpretation
node \(u\). Each row therefore answers:

> In which interpreted structures does this base node occur?

The current graph-level transformer does not construct a separate graph
encoding. It sum-pools the node representation:

\[
x_{P,b}(G)=\sum_{v\in V}Z_{P,b}(G)_{v,:}.
\]

This gives an exact node-to-graph consistency relation and makes node and graph
experiments two views of the same projected representation.

There is, however, an important counting caveat. A raw histogram of structural
occurrences is

\[
h_{P,b,j}(G)=
\sum_{u\in V_I}
\mathbf 1[\phi_b(\mu(u))=j].
\]

Under ordinary unit contributions, sum-pooling the node rows instead gives

\[
x_{P,b,j}(G)=
\sum_{u\in V_I}
|V_{\mu(u)}|
\mathbf 1[\phi_b(\mu(u))=j].
\]

Thus the implemented graph vector is a histogram of **node--structure
incidences**, or equivalently a subgraph-size-weighted occurrence histogram.
It equals the raw occurrence histogram only when every mapped component has one
node, or when each interpretation contribution is normalized by
\(a(u)=1/|V_{\mu(u)}|\). Paper 1 must report which of these two graph-level
encodings is used. Comparing them is a useful aggregation ablation because raw
occurrence counts and incidence mass retain different information.

### Reserved size and degree features

Feature buckets \(0\) and \(1\) receive special treatment and are not available
to structural hashes:

\[
Z_{v,0}=1,
\qquad
Z_{v,1}=\deg_G(v).
\]

After graph-level sum pooling,

\[
x_0(G)=\sum_{v\in V}1=|V|,
\]

so feature \(0\) becomes the graph's node count. Feature \(1\) becomes

\[
x_1(G)=\sum_{v\in V}\deg_G(v)=2|E|.
\]

The last equality holds for NetworkX undirected graphs and for its directed
graphs when `Graph.degree`/`DiGraph.degree` is used: directed total degree is
in-degree plus out-degree, so every edge contributes once at its source and
once at its target. Consequently feature \(1\) is twice the stored edge count,
not \(|E|\). It can be interpreted as the number of directed edge incidences,
or divided by two to recover the edge count. Self-loops also contribute two to
total degree.

These reserved features create a potential shortcut in controlled
discrimination tasks. A classifier could infer a target from graph size or edge
count without using any operator-derived structure. Experiments must therefore
report results both with and without columns \(0\) and \(1\), and hard matched
graph pairs should control \(|V|\) and \(|E|\) whenever the intended distinction
is topological rather than merely cardinal.

### Interpretation-relation features

For relation features,

\[
x_{P,b,(j,k,r)}(G)=
\#\left\{(u,v)\in E_I:
\phi_b(\mu(u))=j,
\phi_b(\mu(v))=k,
R_I(u,v)=r
\right\}.
\]

The vocabulary or vectorizer must be fitted on the training partition only.
Validation and test instances call `transform` without changing the learned
feature space.

## Two complementary definitions of discrimination

### Intrinsic discrimination

For verified non-equivalent graph pairs \(\mathcal{Q}\), define

\[
D_{\mathrm{intrinsic}}(P,b)=
\frac{1}{|\mathcal{Q}|}
\sum_{(G,H)\in\mathcal{Q}}
\mathbf 1[\Sigma_{P,b}(G)\neq\Sigma_{P,b}(H)].
\]

This is a property of the representation and does not require learning. It
directly identifies pairs that a method preserves or collapses.

Intrinsic results must be reported separately by structural factor rather than
only as one aggregate score:

\[
\mathbf d(P)=
(d_{\mathrm{cycle}},d_{\mathrm{path}},d_{\mathrm{ray}},
d_{\mathrm{attachment}},d_{\mathrm{label}}).
\]

### Task-relevant accessibility

A representation may assign different signatures to two graphs while making
the relevant distinction difficult to recover consistently. Simple supervised
probes measure whether controlled properties are accessible from the feature
space.

Primary probes:

- logistic regression for binary properties;
- multinomial logistic regression for structural categories;
- ridge regression for counts and sizes; and
- linear SVM as a margin-based sensitivity analysis.

A random forest is a secondary nonlinear probe. If a linear model fails but a
random forest succeeds, the information may be present only through nonlinear
feature interactions. If both fail and intrinsic signatures are equal, the
program has genuinely collapsed the target distinction. The probes diagnose
the representation; competitive real-world prediction remains Paper 2.

## Controlled synthetic benchmark

The default dataset is `SYN-CPS-01`, generated by
`abstractgraph.artificial.generate_artificial_dataset`. It composes cycles,
paths, and star/ray structures while retaining the actual generating parameters
and component roles in graph metadata.

Controlled factors include:

- cycle presence, length, and count;
- path presence and length;
- ray presence, count, and length;
- attachment arrangement;
- recursive composition depth;
- node- and edge-label alphabet size; and
- shared versus component-specific alphabets.

For each graph \(G\), experiments construct:

1. identifier-permuted copies \(\rho(G)\), which must not be distinguished;
2. semantic attribute-order controls;
3. matched graphs \(G_f\) in which exactly one structural factor changes; and
4. hard matched pairs controlling simple statistics such as node count, edge
   count, degree distribution, density, and label histogram.

Pairs are admitted as discrimination targets only after an exact
attributed-isomorphism check verifies that they are non-equivalent under the
declared attribute projection. The detailed design is in
[`experiments/cycle-path-star.md`](experiments/cycle-path-star.md).

## Baselines as operator expressions

A central contribution is to express adjacent representations in the same
decomposition language. Every expression has three conceptually separate
stages:

\[
\text{decomposition}
\longrightarrow
\text{component identity}
\longrightarrow
\text{aggregation}.
\]

This separation supports controlled ablations: the same decomposition with a
different identity, the same identities with a different aggregation, or
individual components versus relations between components.

| Method | Abstract Graph expression | Structural bias |
| --- | --- | --- |
| Node histogram | `node -> identity -> histogram` | Node-label frequency |
| Edge histogram | `edge -> identity -> histogram` | Labeled adjacency |
| Paths | `path(k) -> path_identity -> histogram` | Sequential connectivity |
| Cycles | `cycle(k) -> graph_identity -> histogram` | Cyclic structure |
| Graphlets | `graphlet(r,k) -> graph_identity -> histogram` | Local induced topology |
| 1-WL subtree features | `repeat(h, neighborhood_labels -> relabel) -> histogram` | Iterated neighborhood-label refinement |
| NSPDK | `neighborhood(r) -> pair_at_distance(d) -> pair_identity -> histogram` | Relations between rooted local neighborhoods |
| Composite Abstract Graph | `add(cycle, path, neighborhood, ...) -> identity` | Explicit multi-view structure |

The WL expression must perform iterative multiset relabelling; ordinary
neighborhood extraction alone is not equivalent to 1-WL. The NSPDK expression
must retain roots, neighborhood radii, root distance, pair identity, and pair
counts.

Expression implementations must be checked against independent reference
implementations using feature multiplicities, graph-pair discrimination
decisions, and kernel or vector values where applicable. Otherwise the
baseline comparison would be circular.

After reproduction, composition experiments extend the named expressions, for
example

\[
P_{\mathrm{WL},h}\oplus P_{\mathrm{cycle}}
\quad\text{or}\quad
P_{\mathrm{NSPDK},r,d}\oplus P_{\mathrm{path},k},
\]

and measure which previously collapsed graph pairs become distinguishable.

## Hash width and feature collapse

Operator composition is not the only source of structural resolution. The
feature identity width \(b=\texttt{nbits}\) controls the number of available
bounded hash buckets,

\[
B=2^b-2.
\]

The analysis must distinguish:

1. **operator collapse:** different graphs produce the same structural
   representation;
2. **certificate collapse:** the identity scheme assigns the same certificate
   to non-equivalent components;
3. **bounded-hash collision:** different certificates map to the same feature
   bucket; and
4. **statistical irrelevance:** a collision occurs but has negligible effect on
   the measured task.

If structural feature frequencies are heavy-tailed, raw collision counts may
overstate downstream distortion. Let \(p_i\) be the empirical frequency of
certificate \(i\). Frequency-weighted collision mass is

\[
C_{\mathrm{mass}}(b)=
\sum_{i<j}p_i p_j
\mathbf 1[h_b(c_i)=h_b(c_j)].
\]

For a frequent feature \(i\), expected contamination from other identities is
approximately ((1-p_i)/B), and its relative contamination is approximately

\[
\frac{1-p_i}{Bp_i}.
\]

This motivates, but does not assume, the hypothesis that frequent identities
are relatively robust while many collisions involve low-frequency tail
features. Rare features may nevertheless be highly predictive, and collisions
can corrupt feature-to-subgraph interpretation even when aggregate prediction
is unchanged.

Evaluate

\[
b\in\{4,6,8,10,12,14,16,20,24,32\}
\]

against a collision-free certificate registry. Report:

- occupied buckets and distinct certificates;
- identity-pair collision rate;
- frequency-weighted collision mass;
- head--head, head--tail, torso--tail, and tail--tail collisions;
- intrinsic discrimination lost to hashing;
- linear and nonlinear probe degradation;
- feature-vector distortion;
- provenance ambiguity; and
- memory and runtime.

The defensible hypothesis is not that collisions never matter. It is:

> Under heavy-tailed structural-feature frequencies, identity-level collision
> counts can substantially exceed frequency-weighted and predictive distortion,
> although rare discriminative structures and exact provenance remain
> vulnerable.

## Discrimination--complexity frontier

For program \(P\) and hash width \(b\), define utility as

\[
U(P,b)=
\left(
D_{\mathrm{intrinsic}},
S_{\mathrm{linear}},
S_{\mathrm{nonlinear}}
\right),
\]

and cost as

\[
C(P,b)=
\left(
T_{\mathrm{representation}},
M_{\mathrm{peak}},
S_{\mathrm{representation}},
N_{\mathrm{features}},
T_{\mathrm{fit}}
\right).
\]

Here \(S_{\mathrm{representation}}\) includes interpretation nodes, relations,
and serialized signature size. A configuration is Pareto-optimal when no other
configuration provides at least as much utility at no greater cost, with one
strict improvement.

Primary Pareto views:

- intrinsic discrimination versus representation runtime;
- linear-probe performance versus representation runtime;
- discrimination versus peak memory;
- discrimination versus representation size; and
- discrimination versus hash width or feature-space size.

Raw cost measurements remain primary; a composite cost score may be shown only
as a secondary summary. Dominated configurations and negative results must be
reported because they reveal where added composition provides little useful
resolution.

## Research questions

### RQ1 — Representation validity

Do unary and multi-input operators preserve the AG validity contracts, mapped
links, and provenance through expression evaluation and serialization?

### RQ2 — Invariance

Do deterministic expressions preserve their representation signatures under
permitted node relabellings and attribute-order changes?

### RQ3 — Programmable discrimination

Which controlled structural distinctions are preserved or collapsed by each
operator expression, and how do alternative compositions modify the induced
partition without assuming an ordered refinement relation?

### RQ4 — Feature accessibility

Which retained distinctions are linearly accessible, require nonlinear feature
interactions, or remain unrecoverable by simple diagnostic probes? How do raw
occurrence pooling, node-incidence pooling, and the reserved size/degree
features change that accessibility?

### RQ5 — Identity width

How do hash width and empirical feature-frequency distributions affect
identity collisions, task performance, and provenance ambiguity?

### RQ6 — Computational trade-off

Which program and identity configurations lie on the discrimination--runtime,
discrimination--memory, and discrimination--size Pareto frontiers?

## Predeclared hypotheses

- **H1:** deterministic reference programs achieve invariant agreement of 1.0
  under permitted relabelling.
- **H2:** an operator targeting a controlled structure increases discrimination
  for that structure relative to expressions that do not expose it; for
  example, a cycle expression distinguishes some pairs collapsed by node,
  degree, or path-only expressions.
- **H3:** every well-typed reference expression is closed over
  \(\mathcal{AG}\): when its operator contracts are satisfied, evaluation
  returns a valid AG with inspectable mappings and provenance. No monotonic
  discrimination hypothesis is attached to composition itself.
- **H4:** linear-probe performance is high when target structures are explicit
  component or relation features; random forests recover some additional
  distinctions through nonlinear interactions.
- **H5:** increasing program depth or structural radius eventually produces
  diminishing discrimination gains relative to runtime and memory.
- **H6:** raw bounded-hash collision counts grow much faster than
  frequency-weighted or predictive distortion under a heavy-tailed feature
  distribution.
- **H7:** the optimal `nbits` value depends on operator-program vocabulary size
  and cannot be selected independently of the expression.
- **H8:** node-incidence pooling favors larger mapped structures relative to raw
  occurrence pooling, while reserved columns \(0\) and \(1\) can create
  size-based shortcuts unless graph pairs are matched on \(|V|\) and \(|E|\).

These are hypotheses, not conclusions. Counterexamples and rejected
hypotheses are reportable results.

## Core figures and tables

1. **Operator-expression diagram:** decomposition, identity, aggregation, and
   mapping back to the base graph.
2. **Discrimination heatmap:** expressions by controlled graph-pair factors,
   showing discrimination and collapse.
3. **Expression trajectories:** utility and cost across related expressions,
   without implying that longer expressions form a refinement chain.
4. **Baseline equivalence table:** reference method, Abstract Graph expression,
   parity tests, and complexity.
5. **Probe accessibility matrix:** intrinsic discrimination, linear probe,
   SVM, and random forest by task.
6. **Pooling ablation:** raw structural occurrences versus summed node incidence,
   with and without reserved node-count and degree columns.
7. **Hash-width curves:** collisions, weighted contamination, probe performance,
   memory, and provenance ambiguity versus `nbits`.
8. **Pareto plots:** non-dominated programs under runtime, memory, and
   representation-size costs.
9. **Failure-case panels:** representative pairs collapsed by one expression
   and separated by another, with responsible mapped subgraphs highlighted.

## Relationship to the claim ledger

The programme claim IDs remain stable, but the experimental emphasis is:

| Claim | Role in this paper |
| --- | --- |
| P1-C1 | Establishes that discrimination remains traceable to base structure. |
| P1-C2 | Establishes closure and the compositional multi-operator language. |
| P1-C3 | Separates structural identity from bounded-hash collision. |
| P1-C4 | Ensures measured discrimination is not caused by node identifiers. |
| P1-C5 | Carries the central discrimination--complexity and Pareto result. |

The authoritative evidence mapping is in
[`../shared/claim-ledger.md`](../shared/claim-ledger.md).

## Scope boundary

This paper covers `abstractgraph` and uses simple estimators only as diagnostic
probes of its feature spaces. It does not claim competitive predictive
performance on real-world targets. The following remain out of scope:

- estimator and feature-selection methodology beyond fixed diagnostic probes;
- learned explanations or attribution quality;
- feasibility modeling;
- graph generation and repair; and
- universal graph-isomorphism discrimination.

Those questions belong to later papers. Paper 1 may use candidate real-world
datasets for structural diversity and scaling validation, but its main causal
evidence comes from controlled synthetic graph pairs.

## Evaluation safeguards

- Freeze graph pairs and semantic attribute projections before comparing
  methods.
- Use exact isomorphism checks to establish pair ground truth.
- Fit feature vocabularies, scalers, and models on training data only.
- Reuse identical splits and seeds across expressions.
- Give probe models and external baselines fixed, comparable budgets.
- Validate expression baselines against independent implementations.
- Separate exploratory pilots from confirmatory runs.
- Report repeated-seed uncertainty and failed runs.
- Record representation time separately from model-fit and inference time.
- Separate method collapse, hash collision, and classifier error.
- Report both raw occurrence and node-incidence pooling where component sizes
  vary.
- Run probe ablations with reserved columns \(0\) and \(1\) removed, and match
  controlled pairs on node and edge counts when those counts are nuisance
  variables.
- Preserve negative results and factor-specific boundary conditions.

## Directory layout

- `manuscript/`: arXiv-compatible LaTeX source with one file per section.
- `specification/`: formalism, implementation inventory, invariants, and
  operator contracts.
- `experiments/`: authoritative manifest, configurations, and controlled
  benchmark designs.
- `analysis/`: metric, table, figure, Pareto, and statistical analysis code.
- `results/`: immutable raw results and run indexes; generated results are not
  hand-edited.
- `figures/`: figure specifications and generated figure index.
- `tables/`: table specifications and generated table index.
- `reproducibility/`: revisions, environments, splits, manifests, and
  completion checklist.

Shared terminology, notation, datasets, baselines, and references live in
[`../shared/`](../shared/README.md).

## Completion gate

The paper is ready for submission only when:

1. the formal definitions and reference expressions match the implementation;
2. baseline expressions reproduce independent implementations within declared
   tolerances;
3. mapping, provenance, serialization, and permutation invariants pass their
   focused tests;
4. controlled discrimination and collapse are reported by structural factor;
5. diagnostic probes use leakage-safe, frozen protocols;
6. node- and graph-level encodings are related explicitly, and pooling plus
   reserved-feature shortcut ablations are reported;
7. the hash-width study separates raw, weighted, predictive, and provenance
   effects;
8. runtime, peak memory, representation size, and model costs are reported;
9. Pareto frontiers include dominated configurations and uncertainty;
10. negative results and practical scaling boundaries are explicit; and
11. every manuscript claim links to immutable evidence in the shared claim
    ledger.
