# AbstractGraph Paper Programme

The execution roadmap is in [PLAN.md](PLAN.md). Resources reused across the
series live in [shared/](shared/README.md), and each paper has an independent
working directory. Paper 1 is being developed in
[paper-01-representation/](paper-01-representation/README.md).

A coherent series should avoid one “everything paper.” The strongest strategy is to introduce the ecosystem as a sequence of increasingly ambitious claims:

1. **representation**
2. **learning**
3. **explanation and feasibility**
4. **generation**
5. **cross-domain unification**

Each paper should stand alone, introduce one central scientific idea, and reuse the same terminology, notation, datasets, and progressively expanded benchmark suite.

## Proposed paper sequence

### Paper 1 — Abstract Graphs as a representation formalism

**Core question:** How can meaningful subgraphs be represented as first-class objects while remaining linked to the original graph?

**Main contribution:** The formal definition of an Abstract Graph as:

* a base graph (G);
* an interpretation graph (I);
* a mapping from each interpretation node to a subgraph of (G);
* composable operators that construct and transform (I).

This paper should establish the mathematical language underlying the whole ecosystem.

Possible title:

> **Abstract Graphs: A Compositional Representation of Graph Structure**

Key scientific claims:

* Graph decompositions can be represented explicitly rather than being discarded after feature extraction.
* Operators over mapped subgraphs form a compositional graph-processing language.
* Structural fragments can be given stable identities through canonicalisation or hashing.
* Derived features remain traceable to their originating nodes and edges.

Experiments should focus on representation, not predictive performance:

* reproducibility of decompositions;
* invariance under node permutation;
* stability of hashed features;
* expressiveness of different operator compositions;
* computational scaling;
* comparison with graphlets, Weisfeiler–Lehman features, motif counting, and graph grammars.

This paper introduces `abstractgraph` only.

---

### Paper 2 — Learning from compositional graph decompositions

**Core question:** Do Abstract Graph representations provide useful and competitive features for graph-level prediction?

**Main contribution:** A general estimator framework that learns over operator-generated graph decompositions.

Possible title:

> **Learning from Abstract Graph Decompositions**

The scientific novelty should not simply be “we apply random forests to graph features.” It should be:

> The decomposition program itself defines an interpretable structural feature space, and predictive learning can be conducted while retaining an exact mapping between model inputs and graph fragments.

Contributions:

* a formal graph-to-feature pipeline;
* support for multi-resolution decomposition;
* feature identities shared across instances;
* integration with classical and neural estimators;
* operator and feature selection;
* analysis of the trade-off between representation complexity and predictive performance.

Experiments could include:

* molecular property prediction;
* protein or RNA classification;
* social or synthetic graph classification;
* controlled synthetic tasks where the true predictive motif is known.

Comparisons:

* WL kernels;
* graphlet kernels;
* GNNs;
* handcrafted domain features;
* possibly tree-based models over conventional graph descriptors.

This introduces `abstractgraph-ml`, but only its estimator and feature-selection components.

---

### Paper 3 — Structural explanations through feature-to-subgraph attribution

**Core question:** Can predictions be explained directly in terms of concrete recurring subgraphs?

**Main contribution:** A method for mapping model relevance back through hashed or vectorised Abstract Graph features to the original graph structures.

Possible title:

> **From Graph Features Back to Graph Structure: Exact Structural Explanations with Abstract Graphs**

This paper should make a stronger scientific contribution than merely visualising feature importance.

Possible method:

* compute feature importance or local attribution;
* resolve each feature to all mapped subgraph occurrences;
* separate global motif importance from instance-specific occurrence importance;
* aggregate overlapping structural explanations;
* quantify explanation stability across folds, models, and graph perturbations.

Potential new concepts:

* **structural attribution consistency**;
* **motif-level fidelity**;
* **explanation compression**, measuring how few mapped subgraphs explain most of a prediction;
* **cross-instance explanation alignment**, identifying recurring predictive structures.

Experiments should use datasets where structural explanations are meaningful and, ideally, partially validated:

* molecular functional groups;
* synthetic graphs with planted motifs;
* protein contact motifs;
* graph classification benchmarks with controlled perturbations.

Comparisons:

* GNNExplainer;
* PGExplainer;
* SubgraphX;
* GraphMask;
* feature attribution over WL or graphlet features.

This paper provides a clear explainable-AI contribution independent of generation.

---

### Paper 4 — Learning graph feasibility from structural components

**Core question:** Can validity or admissibility be learned from recurring local and mesoscopic graph structures?

**Main contribution:** A feasibility model defined over Abstract Graph components that predicts whether a graph, partial graph, or proposed edit is structurally admissible.

Possible title:

> **Learning Structural Feasibility in Graph Space**

This paper could become one of the strongest in the series because feasibility connects descriptive graph analysis to constrained generation.

Possible contributions:

* define structural feasibility at graph, component, and partial-graph levels;
* learn feasibility from observed decompositions;
* identify minimal or near-minimal infeasible component combinations;
* estimate the completion feasibility of partial graphs;
* return interpretable reasons for rejection;
* distinguish hard constraints from learned soft constraints.

Methods might include:

* motif dictionaries;
* one-class models;
* discriminative classifiers;
* energy-based feasibility scoring;
* frequent infeasible substructure mining;
* monotone constraint models;
* conformal calibration for rejection confidence.

Experiments should include controlled synthetic domains where true constraints are known:

* degree-constrained graphs;
* connectedness;
* forbidden motifs;
* chemical valence;
* workflow or DAG constraints;
* abstract component compatibility.

Metrics:

* invalid-graph detection;
* false rejection rate;
* calibration;
* early detection on partial graphs;
* explanation accuracy;
* reduction in wasted generation steps.

This introduces the feasibility part of `abstractgraph-ml`.

---

### Paper 5 — Graph generation by composition of reusable structural units

**Core question:** Can graphs be generated more reliably by assembling meaningful subgraphs rather than predicting individual edges?

**Main contribution:** Conditional autoregressive generation over mapped Abstract Graph components.

Possible title:

> **Compositional Graph Generation with Abstract Graphs**

The central distinction should be explicit:

> Existing graph generators typically operate over nodes, edges, or latent variables. This method operates over reusable, interpretable graph components while preserving their attachment to the evolving base graph.

Contributions:

* autoregressive generation of interpretation-graph components;
* component attachment through ports or interfaces;
* conditional generation from graph-level targets;
* explicit prevention of incompatible compositions;
* exact decoding from interpretation structure to base graph;
* generation traces expressed as meaningful structural decisions.

Experiments:

* synthetic motif-composition datasets;
* molecular generation;
* constrained workflow or DAG generation;
* graph completion;
* generation conditioned on target component histograms.

Comparisons:

* node/edge autoregressive models;
* graph VAEs;
* diffusion-based graph generators;
* grammar-based methods;
* junction-tree or fragment-based molecular generators.

Metrics should include more than validity:

* component-level fidelity;
* structural novelty;
* conditional accuracy;
* diversity;
* reconstruction;
* interpretability of the generation trajectory;
* efficiency under constraints.

This introduces the conditional component generator in `abstractgraph-generative`.

---

### Paper 6 — Constraint-guided graph repair and optimisation

**Core question:** Can infeasible or suboptimal graphs be repaired through interpretable local edits guided by learned feasibility and ranking models?

**Main contribution:** A graph repair framework that identifies problematic structure, removes or rewrites it, and regrows the graph under feasibility and target constraints.

Possible title:

> **Interpretable Graph Repair under Learned Structural Constraints**

This should be framed as more than another generator. Repair is a distinct problem:

[
\text{find } G' \text{ such that } G' \in \mathcal{F}, \quad
d(G,G') \text{ is small}, \quad
s(G') \text{ is high}.
]

Where:

* (\mathcal{F}) is the feasible graph set;
* (d) measures edit cost;
* (s) is a predictive or ranking objective.

Contributions:

* localise feasibility violations to Abstract Graph components;
* derive candidate deletion, substitution, or regrowth regions;
* optimise edit cost and target quality jointly;
* provide a repair trace explaining every modification;
* retrieve compatible structures from related graphs;
* estimate whether a partial repair can still be completed.

Applications:

* molecular validity repair;
* workflow correction;
* graph completion under degree or connectivity constraints;
* infrastructure or network redesign;
* correction of noisy predicted graphs.

Comparisons:

* generic graph edit search;
* beam search;
* MIP or SAT repair where applicable;
* unconstrained regeneration;
* domain-specific repair heuristics.

This paper integrates `abstractgraph`, `abstractgraph-ml`, and `abstractgraph-generative`.

---

### Paper 7 — A cross-domain graph abstraction benchmark

**Core question:** Can the same graph representation and operator language work across fundamentally different data modalities?

**Main contribution:** The graphicalizer layer plus a systematic study of domain-independent graph abstraction.

Possible title:

> **One Graph Language for Heterogeneous Structured Data**

This paper should not merely catalogue converters. It needs a scientific hypothesis:

> Once domain objects are converted into attributed graphs with semantically appropriate labels and relations, the same abstract decomposition, learning, explanation, and feasibility machinery can transfer across domains.

Domains could include:

* molecules;
* proteins;
* RNA;
* tabular feature graphs;
* segmented images;
* attention-derived token graphs;
* conventional networks.

Potential contribution:

* a common graphicalization interface;
* a taxonomy of entity, relation, and attribute choices;
* analysis of how graphicalization decisions affect downstream performance;
* robustness to alternative graph constructions;
* cross-domain operator reuse;
* perhaps transfer of operator programs between domains.

This paper introduces `abstractgraph-graphicalizer` as a scientific study rather than merely a software package.

---

## A possible higher-impact consolidation paper

After the individual methods are established, a final paper could integrate the system:

> **AbstractGraph: An Interpretable Framework for Learning, Generating, and Repairing Structured Objects**

This should not be the first paper. It becomes credible only after the individual claims have been validated.

Its contribution would be the **closed loop**:

[
\text{object}
\rightarrow
\text{graph}
\rightarrow
\text{decomposition}
\rightarrow
\text{learning}
\rightarrow
\text{explanation/feasibility}
\rightarrow
\text{generation or repair}.
]

It could demonstrate one or two complete applications, such as:

* molecular optimisation under structural constraints;
* workflow generation and repair;
* biological graph analysis and constrained generation.

## Recommended publication order

I would use this order:

| Order | Paper                         | Why it comes here                              |
| ----- | ----------------------------- | ---------------------------------------------- |
| 1     | Abstract Graph representation | Establishes notation and foundational object   |
| 2     | Learning from decompositions  | Demonstrates practical value                   |
| 3     | Structural explanations       | Exploits traceability as a distinctive benefit |
| 4     | Structural feasibility        | Introduces constraints and prepares generation |
| 5     | Compositional generation      | Uses representation and feasibility            |
| 6     | Graph repair and optimisation | Integrates the full methodology                |
| 7     | Cross-domain graphicalization | Shows generality after the methods are mature  |
| 8     | Integrated ecosystem paper    | Presents the complete scientific programme     |

Papers 2 and 3 could potentially be reversed. However, publishing prediction before explanation usually makes the explanation paper easier to motivate.

## Terminology that should remain fixed across papers

To make the series feel like one programme, use the same core vocabulary throughout:

* **base graph**: the original attributed graph;
* **interpretation graph**: graph whose nodes represent mapped subgraphs;
* **mapped subgraph**: a structural component tied to a region of the base graph;
* **operator**: a composable transformation or decomposition;
* **operator program**: a sequence or composition of operators;
* **structural feature identity**: canonical or hashed identity of a mapped component;
* **feasibility model**: model of admissible graph structure;
* **constructive operator**: operation that adds, removes, replaces, or joins components;
* **repair trace**: interpretable sequence transforming an input graph into a feasible graph.

Avoid changing between terms such as “abstract node,” “motif node,” “component node,” and “interpretation node” unless they denote genuinely different objects.

## What each paper must add

A useful test is that every paper should have a sentence of this form:

> Previous papers enabled (X); this paper introduces (Y), which makes it possible to (Z).

For example:

* Paper 1: mapped structural representations.
* Paper 2: predictive learning over those representations.
* Paper 3: exact return from predictions to concrete structure.
* Paper 4: learned admissibility over partial and complete graphs.
* Paper 5: generation through structural composition.
* Paper 6: targeted correction rather than generation from scratch.
* Paper 7: transfer of the entire abstraction across domains.

## My strongest recommendation

The first three papers should be tightly linked and relatively conservative:

1. **formalism and operators**;
2. **predictive learning**;
3. **structural explanations**.

Then the more ambitious second wave should be:

4. **feasibility**;
5. **generation**;
6. **repair**.

That gives the programme a natural scientific progression:

> represent structure → learn from structure → explain with structure → constrain structure → generate structure → repair structure.

The most distinctive long-term claim is not any individual algorithm. It is that **the same explicit structural objects can support representation, prediction, explanation, validity, generation, and intervention without abandoning traceability to the original graph**.
