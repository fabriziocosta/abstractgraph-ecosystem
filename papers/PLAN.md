# AbstractGraph Papers Plan

This plan turns the proposed paper sequence in [README.md](README.md) into an
execution roadmap. The programme advances one cumulative claim:

> The same explicit structural objects can support representation, prediction,
> explanation, feasibility, generation, and repair while remaining traceable to
> the original graph.

## Programme principles

- Each paper must stand alone and make one central scientific claim.
- Later papers may depend on established methods, notation, datasets, and
  software, but must contribute a new method or scientific finding.
- Terminology, notation, dataset splits, and evaluation protocols must remain
  consistent across the series.
- Claims must be supported by controlled synthetic experiments and at least one
  meaningful real-world domain where appropriate.
- Every reported experiment must be reproducible from a versioned
  configuration, fixed seed policy, recorded environment, and immutable result
  artifact.
- Software required by a paper must have focused tests and a stable public API
  before the paper is submitted.

## Fixed vocabulary

Use these terms consistently in manuscripts, code, figures, and documentation:

| Term | Meaning |
| --- | --- |
| Base graph | The original attributed graph. |
| Interpretation graph | A graph whose nodes represent mapped subgraphs. |
| Mapped subgraph | A structural component tied to a region of the base graph. |
| Operator | A composable transformation or decomposition. |
| Operator program | A sequence or composition of operators. |
| Structural feature identity | The canonical or hashed identity of a mapped component. |
| Feasibility model | A model of admissible graph structure. |
| Constructive operator | An operation that adds, removes, replaces, or joins components. |
| Repair trace | An interpretable sequence transforming an input graph into a feasible graph. |

Do not use “abstract node,” “motif node,” “component node,” and “interpretation
node” interchangeably unless the manuscript explicitly defines distinct
objects.

## Dependency map

```text
Paper 1: representation
  -> Paper 2: learning
       -> Paper 3: explanation
       -> Paper 4: feasibility
            -> Paper 5: generation
                 -> Paper 6: repair

Papers 1-6
  -> Paper 7: cross-domain benchmark
       -> Paper 8: integrated ecosystem paper
```

Paper 3 can begin alongside Paper 2 once feature identities and provenance are
stable. Paper 7 dataset adapters can be developed earlier, but its scientific
comparison should wait until the common methods and protocols are mature.

## Shared foundations

Complete these foundations once and reuse them throughout the programme.

### Scientific specification

- [ ] Write a notation guide defining the base graph, interpretation graph,
  mappings, operators, operator programs, identities, and provenance.
- [ ] State the invariants expected of every operator and mapping.
- [ ] Define the boundary between a representation result, a predictive result,
  an explanation, a feasibility decision, and a constructive action.
- [ ] Maintain a claim ledger linking every manuscript claim to experiments,
  tables, figures, and supporting artifacts.

### Reproducible experiment system

- [ ] Standardise configuration, random seeds, dataset split storage, result
  schemas, logging, and environment capture across repositories.
- [ ] Create a dataset registry recording source, licence, version, processing,
  graph construction, task, split, and known limitations.
- [ ] Create a benchmark registry recording baselines, versions,
  hyperparameter budgets, metrics, and evaluation rules.
- [ ] Store raw results separately from analysis and manuscript figures.
- [ ] Add smoke tests for every experiment pipeline and deterministic tests for
  metrics and data transformations.

### Shared benchmark design

- [ ] Build controlled synthetic generators with known motifs, constraints, and
  causal labels.
- [ ] Select a compact initial real-world suite spanning molecules and at least
  one non-molecular graph domain.
- [ ] Freeze common train/validation/test splits before comparative experiments.
- [ ] Define compute budgets and a fair hyperparameter-selection protocol.
- [ ] Record representation time, training time, inference time, peak memory,
  and scaling alongside task-specific metrics.

### Manuscript infrastructure

- [ ] Adopt one paper template, bibliography database, notation file, and figure
  style.
- [ ] Create a directory per paper containing manuscript source, experiment
  manifest, figure-generation entry points, and a reproducibility checklist.
- [ ] Maintain a shared related-work matrix so comparisons and terminology do
  not drift between papers.
- [ ] Version all paper snapshots against exact repository commits.

## Paper roadmap

### Paper 1 — Abstract Graphs: A Compositional Representation of Graph Structure

**Claim:** Explicit mapped decompositions form a reproducible, compositional,
traceable, and computationally usable representation of graph structure.

**Software scope:** `abstractgraph` only.

#### Deliverables

- [ ] Formal definition of the base graph, interpretation graph, mapping, and
  operator composition.
- [ ] Algebra or typed semantics for valid operator programs.
- [ ] Canonicalisation and structural identity specification.
- [ ] Provenance model linking derived components to original nodes and edges.
- [ ] Reference operator suite with invariance and provenance tests.
- [ ] Complexity analysis for core operators and identity construction.

#### Experiments

- [ ] Reproducibility of decompositions across runs and serialisation cycles.
- [ ] Invariance under node permutation and robustness to attribute ordering.
- [ ] Collision and stability analysis for structural feature identities.
- [ ] Expressiveness study across operator programs.
- [ ] Runtime and memory scaling by graph size, density, and program depth.
- [ ] Comparison with graphlets, Weisfeiler–Lehman features, motif counting,
  and graph grammars.

#### Completion gate

Proceed when definitions and invariants match the implementation, identities
are empirically stable, provenance is exact, scaling limits are documented, and
all main claims have a corresponding experiment or theorem.

### Paper 2 — Learning from Abstract Graph Decompositions

**Claim:** Operator programs define competitive, interpretable structural
feature spaces while preserving exact links from model inputs to graph
fragments.

**Software scope:** `abstractgraph` and the estimator/feature-selection parts of
`abstractgraph-ml`.

#### Deliverables

- [ ] Formal graph-to-feature pipeline with shared identities across instances.
- [ ] Multi-resolution decomposition and vectorisation.
- [ ] Classical estimator interface and selected neural integration.
- [ ] Operator, feature, and resolution selection procedures.
- [ ] Leakage-safe fit/transform semantics for learned vocabularies.

#### Experiments

- [ ] Controlled motif tasks with known predictive structure.
- [ ] Molecular property prediction.
- [ ] One biological or conventional graph-classification task.
- [ ] Comparison with WL kernels, graphlet kernels, GNNs, conventional graph
  descriptors, and relevant domain features.
- [ ] Ablations over operators, program depth, resolution, identity scheme, and
  feature selection.
- [ ] Accuracy/complexity trade-off and sample-efficiency analysis.

#### Completion gate

Proceed when the representation is competitive on a predeclared subset of
tasks, the comparison budget is fair, feature provenance survives the complete
learning pipeline, and ablations identify where the method helps or fails.

### Paper 3 — Exact Structural Explanations with Abstract Graphs

**Claim:** Model relevance can be returned exactly to recurring structural
components and their concrete occurrences, enabling stable global and local
graph explanations.

**Software scope:** attribution and importance components of
`abstractgraph-ml`, using Papers 1-2 foundations.

#### Deliverables

- [ ] Feature-to-occurrence resolution for global and local explanations.
- [ ] Rules for aggregating overlapping mapped subgraphs.
- [ ] Definitions of structural attribution consistency, motif-level fidelity,
  explanation compression, and cross-instance explanation alignment.
- [ ] Model-agnostic and model-specific attribution paths where justified.

#### Experiments

- [ ] Recovery of planted explanatory motifs.
- [ ] Molecular functional-group explanations or another expert-validatable
  domain.
- [ ] Stability across folds, models, seeds, and graph perturbations.
- [ ] Fidelity, sparsity/compression, runtime, and alignment evaluation.
- [ ] Comparison with GNNExplainer, PGExplainer, SubgraphX, GraphMask, and
  attribution over WL or graphlet features.

#### Completion gate

Proceed when explanation ground truth is explicit for synthetic tasks, exact
provenance is distinguished from attribution quality, and the proposed metrics
show both strengths and failure cases.

### Paper 4 — Learning Structural Feasibility in Graph Space

**Claim:** Admissibility of complete and partial graphs can be learned from
local and mesoscopic structural components with calibrated, interpretable
rejection reasons.

**Software scope:** feasibility components of `abstractgraph-ml`.

#### Deliverables

- [ ] Formal graph-, component-, and partial-graph feasibility tasks.
- [ ] Hard-constraint and learned soft-constraint interfaces.
- [ ] At least two model families selected from discriminative, one-class,
  energy-based, monotone, or substructure-mining approaches.
- [ ] Infeasible-component localisation and rejection explanations.
- [ ] Completion-feasibility estimator for partial graphs.
- [ ] Calibrated confidence or conformal rejection mechanism.

#### Experiments

- [ ] Known constraints: degree, connectedness, forbidden motifs, and DAG rules.
- [ ] At least one domain constraint such as chemical valence or workflow
  compatibility.
- [ ] Complete-graph detection and early partial-graph detection.
- [ ] False rejection, calibration, explanation accuracy, and avoided invalid
  construction steps.
- [ ] Ablation of component scale and hard/soft constraint combinations.

#### Completion gate

Proceed when feasibility is evaluated separately from ordinary classification,
partial-graph decisions are calibrated, and rejection explanations can be
checked against known violations.

### Paper 5 — Compositional Graph Generation with Abstract Graphs

**Claim:** Generating reusable mapped components and their interfaces yields
valid, controllable, and interpretable construction trajectories.

**Software scope:** conditional component generation in
`abstractgraph-generative`, supported by `abstractgraph` and feasibility models.

#### Deliverables

- [ ] Component vocabulary and attachment-port/interface representation.
- [ ] Autoregressive interpretation-graph generator.
- [ ] Exact decoder from interpretation structure to base graph.
- [ ] Conditional generation and compatibility filtering.
- [ ] Persisted generation trace expressed as structural decisions.

#### Experiments

- [ ] Synthetic motif-composition benchmark.
- [ ] Molecular or workflow/DAG generation.
- [ ] Graph completion and target component-histogram conditioning.
- [ ] Comparison with node/edge autoregression, graph VAEs, diffusion,
  grammar-based methods, and relevant fragment-based generators.
- [ ] Validity, novelty, diversity, conditional accuracy, reconstruction,
  component fidelity, efficiency, and trajectory interpretability.

#### Completion gate

Proceed when decoding is exact for supported compositions, compatibility rules
are evaluated independently from learned generation, and gains are not solely
explained by the component vocabulary or feasibility filter.

### Paper 6 — Interpretable Graph Repair under Learned Structural Constraints

**Claim:** Infeasible or suboptimal graphs can be corrected through minimal,
interpretable structural edits guided by feasibility and target objectives.

**Software scope:** integration of `abstractgraph`, `abstractgraph-ml`, and
`abstractgraph-generative`.

#### Deliverables

- [ ] Repair objective balancing feasibility, edit distance, and target score.
- [ ] Violation localisation and candidate deletion, substitution, and regrowth.
- [ ] Search/ranking procedure with completion-feasibility pruning.
- [ ] Compatible-component retrieval from related graphs.
- [ ] Complete repair trace and failure diagnosis.

#### Experiments

- [ ] Synthetic corruption with known minimal repairs.
- [ ] At least two applications from molecular repair, workflow correction,
  constrained completion, network redesign, or noisy graph correction.
- [ ] Comparison with graph edit search, beam search, MIP/SAT where applicable,
  unconstrained regeneration, and domain heuristics.
- [ ] Feasibility recovery, edit cost, objective improvement, success rate,
  search cost, and trace accuracy.

#### Completion gate

Proceed when minimality or bounded suboptimality can be measured on controlled
tasks, repair is demonstrably different from regeneration, and each edit is
linked to a diagnosed violation or declared target objective.

### Paper 7 — One Graph Language for Heterogeneous Structured Data

**Claim:** Semantically appropriate graphicalization permits reuse of the same
operator, learning, explanation, and feasibility machinery across domains.

**Software scope:** `abstractgraph-graphicalizer` plus stable methods from the
preceding papers.

#### Deliverables

- [ ] Common graphicalization interface and metadata contract.
- [ ] Taxonomy of entity, relation, label, and attribute choices.
- [ ] Documented adapters for a deliberately diverse domain set.
- [ ] Protocol for sensitivity to alternative graph constructions.
- [ ] Cross-domain operator-program transfer procedure.

#### Experiments

- [ ] Select at least four substantively different modalities.
- [ ] Compare alternative graph constructions within each domain.
- [ ] Measure downstream sensitivity, robustness, and operator reuse.
- [ ] Test transfer of operator programs or program priors between domains.
- [ ] Compare common machinery with domain-specific representations and
  features.

#### Completion gate

Proceed when “domain-independent” is supported by predeclared transfer or reuse
criteria, graphicalization choices are treated as experimental variables, and
the work demonstrates more than a catalogue of converters.

### Paper 8 — Integrated AbstractGraph Ecosystem

**Claim:** A single traceable structural abstraction supports a closed loop from
domain objects through learning and explanation to constrained construction or
repair.

**Timing:** Begin only after the individual methods have been independently
validated.

#### Deliverables

- [ ] Unified formal and software architecture.
- [ ] One or two complete applications spanning graphicalization,
  decomposition, learning, explanation/feasibility, and generation/repair.
- [ ] End-to-end provenance connecting final decisions and edits to source
  objects.
- [ ] Consolidated limitations, governance, reproducibility, and extension
  guidance.

#### Completion gate

Submit only when the integration produces a scientific result not obtainable by
placing prior paper summaries side by side.

## Cross-paper evaluation rules

- Predeclare primary and secondary metrics for each task.
- Separate confirmatory experiments from exploratory analysis.
- Use identical splits and evaluation code when a dataset appears in multiple
  papers.
- Give baselines comparable tuning budgets and report unsuccessful runs.
- Report confidence intervals or repeated-seed variation, not only point
  estimates.
- Include negative results and boundary conditions relevant to the central
  claim.
- Treat provenance correctness, calibration, compute, and scaling as first-class
  outcomes rather than supplementary details.
- Do not reuse test sets for method selection across the sequence.

## Near-term work plan

### Phase 0 — Programme setup

- [ ] Create the notation guide and claim ledger.
- [ ] Inventory implemented operators, identities, mappings, serialisation, and
  provenance in `abstractgraph`.
- [ ] Map every proposed Paper 1 claim to current implementation evidence or a
  missing capability.
- [ ] Select synthetic generators and candidate real-world datasets.
- [x] Establish experiment and manuscript directory conventions.

### Phase 1 — Paper 1 specification and evidence

- [ ] Freeze the formal object model and operator invariants.
- [ ] Build correctness, permutation-invariance, identity-stability, and
  provenance test suites.
- [ ] Implement scaling benchmarks and baseline representations.
- [ ] Run pilot experiments to identify unsupported claims and practical limits.
- [ ] Draft definitions, methods, and experiment protocol before full runs.

### Phase 2 — Paper 1 completion and Paper 2 pilot

- [ ] Freeze Paper 1 experiments and generate final artifacts.
- [ ] Complete the Paper 1 manuscript and reproducibility package.
- [ ] In parallel, validate leakage-safe vectorisation and shared feature
  identities for Paper 2.
- [ ] Run one planted-motif task and one real-world prediction pilot.

## Immediate next actions

1. Write the shared notation and invariants document.
2. Produce a feature inventory of `abstractgraph` against Paper 1 deliverables.
3. Choose the first synthetic benchmark and specify its expected invariances.
4. Choose two identity baselines and two decomposition baselines.
5. Create the Paper 1 experiment manifest before implementing new experiments.

## Decision log

Record consequential changes here so the paper sequence does not drift without
an explicit rationale.

| Date | Decision | Rationale | Affected papers |
| --- | --- | --- | --- |
| YYYY-MM-DD | Initial eight-paper sequence adopted | Establish representation before progressively adding learning, explanation, feasibility, construction, and integration. | 1-8 |
