# Paper 1 — Composing mapped structural graph representations

Working title:

> **Abstract Graphs: Composing Mapped Structural Representations**

Alternative, more conservative title:

> **Abstract Graphs: A Compositional Representation of Graph Structure**

## Paper in one paragraph

An Abstract Graph (AG) couples a base graph with an interpretation graph whose
nodes refer back to structures in the base graph. This common graph-valued
representation makes heterogeneous structural operators composable without
discarding their source mappings. The paper asks whether that construction does
more than organize familiar feature extractors. It tests exact translations of
established representations, compares graph-valued composition with atomic
features and lossless feature concatenation, and checks whether mapped witnesses
localize the structural intervention responsible for a distinction. The useful
outcome is not a universal expressivity order, but a measured account of which
distinctions an expression exposes and what runtime, memory, and representation
size they require.

## Central scientific question

> Does a common mapped, graph-valued operator language enable faithful baseline
> representations and compositional distinctions beyond flat feature union,
> and what do those distinctions cost?

This question has three parts:

1. **Resolution:** which controlled structural changes alter the representation?
2. **Accessibility:** are those changes directly recoverable from the feature
   space by a simple model?
3. **Cost:** what runtime, memory, and representation size are required?

## Central claim

> **A common mapped, graph-valued operator language makes structural
> representation choices explicit and composable. Different expressions can
> induce distinct and incomparable discrimination profiles; the experiments
> test whether genuine composition adds localized distinctions beyond atomic
> representations and lossless feature concatenation, and at what cost.**

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

Closure is a formal property of the construction, not an empirical result.
There is no universal order
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

This narrow interface lowers the implementation burden of encoding domain
knowledge. Ease of authoring and automatically generated operators are not
claims evaluated in Paper 1.

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

If a linear probe fails although intrinsic signatures differ, the result is
reported as inaccessible to that probe rather than as representation collapse.
The probes diagnose the representation; competitive real-world prediction and
nonlinear model selection remain Paper 2.

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

## Natural molecular graphs

The selected natural corpus is `ZINC-250K-01`. Paper 1 loads the local
`zinc_250k` CSV export through
`abstractgraph_graphicalizer.chem.ZINCLoader`; cached node-count buckets use
`abstractgraph_graphicalizer.chem.load_zinc_graph_dataset`. Dataset parsing and
SMILES-to-NetworkX conversion therefore remain in the graphicalizer rather than
being duplicated in experiment notebooks.

ZINC complements rather than replaces the artificial generator. Synthetic
one-factor pairs support causal statements about which distinction an operator
exposes. ZINC tests structural-certificate frequencies, vocabulary and sparse
representation size, hash-width behavior, and computational scaling. It does
not supply causal evidence about a named structural intervention. Its molecular
property columns are not prediction targets in Paper 1.

Confirmatory runs must freeze the CSV checksum, graphicalizer and chemistry
toolkit versions, skipped SMILES, attribute projection, duplicate policy,
molecule IDs, subset seed, and subset manifest.

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

against an unbounded certificate registry whose equality has been validated
against exact attributed isomorphism on the evaluated component suite. This
registry removes bounded hashing but is not assumed to solve canonical graph
identity beyond the declared equivalence. Report:

- occupied buckets and distinct certificates;
- identity-pair collision rate;
- frequency-weighted collision mass;
- head--head, head--tail, torso--tail, and tail--tail collisions;
- intrinsic discrimination lost to hashing;
- linear-probe degradation;
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

Traceability follows from the mapped Abstract Graph construction, and
permutation equivariance is required of admissible structural operators. Their
implementation is covered by software and serialization tests rather than
treated as an empirical contribution.

### RQ1 — Structural discrimination

Can faithful Abstract Graph expressions expose and localize structural
distinctions that their atomic components and lossless feature concatenation do
not?

This question includes intrinsic graph-pair discrimination, accessibility to
linear probes, occurrence versus incidence pooling, the reserved
size and degree features, and the distinction between operator collapse and
bounded-hash collisions.

### RQ2 — Discrimination--complexity trade-off

What computational cost is required for each factor-specific discrimination
gain, and do graph-valued compositions occupy frontier points unavailable to
their atomic and concatenated controls?

## Predeclared hypotheses

- **H1:** the declared Abstract Graph translations reproduce the feature
  multiplicities and pair decisions of independent WL, path, and NSPDK
  implementations.
- **H2:** discrimination profiles of alternative operator expressions are
  generally incomparable: each of two expressions can distinguish controlled
  pairs collapsed by the other.
- **H3:** at least one graph-valued composition separates a held-out structural
  contrast that its atomic expressions and their lossless feature concatenation
  collapse; otherwise composition is supported only as an organizational
  abstraction.
- **H4:** mapped witnesses for representative distinctions overlap the known
  synthetic intervention more accurately than an unmapped graph-level
  signature can localize it.
- **H5:** increasing program depth or structural radius eventually produces
  diminishing discrimination gains relative to runtime and memory.
- **H6:** raw bounded-hash collision counts grow much faster than
  frequency-weighted or predictive distortion under a heavy-tailed feature
  distribution.
- **H7:** node-incidence pooling favors larger mapped structures relative to raw
  occurrence pooling, while reserved columns \(0\) and \(1\) can create
  size-based shortcuts unless graph pairs are matched on \(|V|\) and \(|E|\).

These are hypotheses, not conclusions. Counterexamples and rejected
hypotheses are reportable results.

## Evidence plan: figures and tables

The main paper should use a small sequence of artifacts that builds the
argument. Additional diagnostics belong in the appendix rather than competing
with the central discrimination--complexity result.

### Essential main-text figures

#### Figure 1 — One graph pair, several structural views

- File: `fig01-structural-views.pdf`
- LaTeX label: `fig:structural-views`

Start from a predeclared matched pair with the same node count, edge count, and preferably
degree distribution, but different cycle or attachment structure. Show the two
base graphs, the mapped structures selected by at least two expressions, and
their resulting interpretation graphs or signatures. One expression should
collapse the pair and another should separate it. An additional panel should
show that both outputs remain Abstract Graphs and can therefore be passed to a
subsequent operator.

Mark the known intervention and the mapped witness returned by the separating
expression, and report their overlap. This figure introduces discrimination and
tests the diagnostic value of the mapping through a concrete example. It should
replace a generic software-pipeline diagram.

#### Figure 2 — Structural discrimination atlas

- File: `fig02-discrimination-atlas.pdf`
- LaTeX label: `fig:discrimination-atlas`

Construct a heatmap with operator and baseline expressions as rows and
controlled structural interventions as columns. Columns should include cycle
count and length, path length, ray count and length, attachment pattern,
semantic labels, and hard pairs matched on simple graph statistics. Each cell
reports intrinsic discrimination using collision-free structural identities.

Group related expressions visually: counts, neighborhoods, paths, cycles,
graphlets, WL, NSPDK, and composites. The intended result is a set of distinct
and potentially incomparable discrimination profiles, not a total ranking.

#### Figure 3 — Pairwise changes under composition

- File: `fig03-composition-transitions.pdf`
- LaTeX label: `fig:composition-transitions`

For each pair of atomic expressions, compare the atoms, their lossless feature
concatenation, and graph-valued composition. Classify controlled graph pairs
into four outcomes relative to each control:

- remained collapsed;
- became distinguishable;
- remained distinguishable; and
- became collapsed.

Display these outcomes as transition matrices or aligned stacked bars. Add one
mapped witness of a gained distinction and one of a lost distinction, marking
the known intervention and reporting witness overlap. This figure must make
clear whether composition contributes anything beyond flat feature union. A
plot showing only gains, or omitting concatenation, is insufficient.

#### Figure 4 — Discrimination--complexity Pareto frontiers

- File: `fig04-pareto-frontiers.pdf`
- LaTeX label: `fig:pareto-frontiers`

Use aligned panels for factor-specific intrinsic discrimination against
runtime, peak memory, and representation size; keep any aggregate panel
secondary. A point represents a complete configuration,
including the expression, depth or radius, identity width, and pooling rule.
Include atomic and concatenated controls. Use consistent colors for expression families, mark non-dominated points, and
label a small number of interpretable cases: the cheapest baseline, a strong
single operator, a useful composite, and an expensive configuration with little
additional discrimination.

This figure provides the primary answer to RQ2. Raw cost dimensions must remain
separate; a composite cost score may appear only as a secondary analysis.

### Conditional main-text figure

#### Figure 5 — Intrinsic discrimination versus predictive accessibility

- File: `fig05-predictive-accessibility.pdf`
- LaTeX label: `fig:predictive-accessibility`

Compare intrinsic discrimination with linear-probe performance, using facets
or marker styles for occurrence versus incidence pooling and reserved features
included versus removed. Highlight genuine representational collapse,
linearly accessible information, information retained but inaccessible to the
probe, and apparent success caused by node-count or degree shortcuts.

Keep this figure in the main text only if it reveals a clear distinction between
representation capacity and model accessibility. Otherwise retain one concise
panel and move the full matrix to the appendix.

### Essential main-text tables

#### Table 1 — Baselines as Abstract Graph expressions

- File: `tab01-baseline-expressions.tex`
- LaTeX label: `tab:baseline-expressions`

For every adjacent method, report its Abstract Graph expression, selected
structural object, identity rule, aggregation rule, and independent parity
test. The minimum set is node/degree features, paths, WL, and NSPDK; cycles are
the principal domain-specific operator. Graphlets enter only if their
translation adds a distinct comparison. A method enters the comparison only after feature multiplicities,
graph-pair decisions, or kernel/vector values agree with an independent
implementation under the declared tolerance.

#### Table 2 — Representative expression trade-offs

- File: `tab02-expression-tradeoffs.tex`
- LaTeX label: `tab:expression-tradeoffs`

Select a small, interpretable set of configurations rather than reproducing the
full grid. Include atomic, concatenated, and graph-composed versions of the same
views. For each, report the distinctions exposed, factor-specific discrimination,
linear accessibility, runtime, memory, representation size, and Pareto status.
Include simple baselines, WL, paths, cycles, NSPDK, useful composites, and at
least one illustrative dominated configuration.

### Appendix figures and tables

The appendix should contain the complete operator-by-factor matrix, all probe
metrics and hyperparameters, full pooling and reserved-feature ablations,
complete complexity and failure-boundary tables, scaling curves by graph size
and density, and additional mapped graph-pair examples.

Hash-width curves should report raw identity collisions, frequency-weighted
contamination, predictive distortion, memory, and provenance ambiguity against
`nbits`. Promote this analysis to a main-text figure only if it supports a clear
result---for example, raw collisions rising much earlier than weighted or
predictive distortion. Otherwise it remains a robustness analysis under RQ1.
Its canonical appendix artifact is `figA01-hash-width-curves.pdf` with LaTeX
label `fig:appendix-hash-width`.

Every generated artifact must record its source run IDs, configuration digests,
and generating notebook. Figures and numerical tables must not be edited by
hand after generation.

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
