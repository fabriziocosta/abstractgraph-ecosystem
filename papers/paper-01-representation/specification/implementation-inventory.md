# Paper 1 implementation inventory

Audit date: 2026-07-14

Audited repository: `repos/abstractgraph`

Audited revision: `d221034a26950487622579701e105a0672029770`, with an
existing dirty worktree affecting `decomposition_graph.png`, one example
notebook, and `src/abstractgraph/display.py`. Those changes were not made or
modified by this audit. Findings describe the working tree visible on the audit
date; final evidence must be tied to a clean, recorded revision.

## Status vocabulary

- **Implemented:** a concrete public or internal implementation exists.
- **Partial:** relevant implementation exists, but it does not yet meet the
  Paper 1 specification or evidence requirement.
- **Missing:** no implementation or artifact meeting the requirement was found.
- **Unverified:** code or tests exist, but they could not be executed in the
  current environment.

This is a capability inventory, not evidence that the scientific claims are
confirmed.

## Executive assessment

The repository already contains the main ingredients of the proposed
representation: a two-level graph object, mapped subgraphs, a large operator
suite, higher-order composition, bounded structural hashes, operator-program
XML serialization, and metadata that records the producing operator. The
current implementation is therefore sufficient to draft an implementation-led
formal specification and to construct pilot experiments.

The main gaps are scientific contracts and evidence. Mapping validity is not
enforced globally, operator typing is informal and runtime-only, structural
equivalence and collision policy are not frozen, provenance is metadata rather
than a validated node-and-edge lineage model, and only operator programs---not
complete Abstract Graph states---have an explicit serialization round trip. No
scaling benchmark or baseline comparison implementation was found.

## Capability matrix

| Paper 1 requirement | Status | Current implementation | Evidence or gap |
| --- | --- | --- | --- |
| Base graph | Implemented with restricted scope | `AbstractGraph.base_graph` stores a copy of a NetworkX `Graph` or `DiGraph`; `is_simple_graph` rejects `MultiGraph` and `MultiDiGraph`. | Directed and undirected simple graphs are supported. Multigraphs, hypergraphs, and a formal attribute domain are outside the current contract. See `src/abstractgraph/graphs.py`. |
| Interpretation graph | Partial | `AbstractGraph.interpretation_graph` is a simple, undirected NetworkX `Graph`. Nodes may contain `mapped_subgraph`, `label`, `attribute`, and `meta`; edge functions can add relations. | Interpretation-edge semantics and allowed attributes are not formally typed. The interpretation graph remains undirected even for directed base graphs. |
| Mapping to base subgraphs | Partial | The mapping is materialized as each interpretation node's `mapped_subgraph` payload. Helpers construct full-graph, node-induced, edge-induced, or supplied subgraphs. Inverse node mappings can be computed. | There is no first-class mapping object or global validator. `create_interpretation_node_with_subgraph_from_subgraph` accepts an arbitrary graph without checking membership in the base graph or copying it. Empty, disconnected, overlapping, and whole-graph mappings are possible but not governed by a frozen contract. Base-edge inverse mappings are not exposed. |
| Operator interface | Partial | Operators are callables from `AbstractGraph` to `AbstractGraph`; four scaffold helpers distinguish local/global and node/edge component materialization. Decomposition helpers require concrete list outputs. | Contracts are conventions enforced unevenly at runtime. There is no explicit input/output type algebra, validity predicate, standardized failure taxonomy, or machine-readable contract beyond directed-support metadata. |
| Operator composition | Implemented, specification pending | `add`, reverse-order `compose`, `forward_compose`, and `compose_product` provide additive, sequential, and parallel composition. Conditionals and loops are also present. | Algebraic laws such as closure, associativity conditions, identity behavior, and equivalence are not stated or proved. Deduplication is an implicit default in composition and must be included in the semantics. |
| Reference operator suite | Implemented, incompletely evidenced | The XML registry contains 54 operators covering composition/control flow, decompositions, graph transforms, filters, binary operations, relabeling, and metadata. Each registered operator has one of five directed-support declarations. | Coverage is concentrated in a single test module. Per-operator mapping validity, determinism, permutation invariance, provenance, and failure behavior are not systematically tested. The manuscript should select a smaller normative reference subset rather than claim all 54 equally. |
| Directedness contract | Implemented | Operators declare `agnostic`, `preserve`, `weak`, `directed`, or `undirected_only`; runtime validation rejects unsupported directed inputs. | The meaning of each mode needs a formal definition. Tests cover representative directed operations and registry completeness, not every operator's semantics. |
| Structural feature identity | Partial | `hash_graph` exposes `fast` and `canonical` modes. Hashing incorporates topology, directedness, and the node/edge `label` attribute, then bounds results to `nbits`. Alternative identities use operator names or node-label histograms. | Only the `label` attribute participates in graph identities; other attributes are ignored. The intended equivalence relation is not frozen. Bounded hashes necessarily collide, but no collision-detection or resolution policy exists. The default is the faster mode, while the stronger canonical mode may branch heavily on symmetric graphs. |
| Canonicalisation | Partial | Values receive deterministic type-tagged JSON encodings. The canonical graph mode builds rooted hashes and a relabeling-oriented DFS certificate without node IDs as tie-breakers. | There is no proof or exhaustive validation that the graph certificate is a complete canonical form for the declared graph class. Complexity in tied neighborhoods is described qualitatively, not bounded for the manuscript. |
| Provenance | Partial | Scaffolded operators attach `source_function`, parameters, a serialized `source_chain`, and sometimes a copied `parent_mapped_subgraph` under interpretation-node `meta`. Mapped subgraphs retain original base node and edge identifiers when constructed from the base graph. | There is no explicit provenance type, validator, or composition theorem. Provenance completeness for both nodes and edges is not tested systematically. Global operators can omit the parent subgraph, arbitrary supplied subgraphs can break lineage, and copied parent graphs are expensive and do not encode a normalized derivation DAG. |
| Operator-program serialization | Implemented, incompletely evidenced | `xml.py` serializes and deserializes registered operator trees, parameters, callables by registry reference, metadata, combiners, conditionals, and loops. File and string APIs exist. | Tests cover a limited set of round trips. Equivalence of behavior before and after serialization is not tested across the full reference suite. Registry references and user-defined callables constrain portability. |
| Abstract Graph state serialization | Missing | No explicit serializer/deserializer for `base_graph`, `interpretation_graph`, mappings, labels, attributes, and provenance was found. | The planned decomposition serialization-cycle experiment cannot currently test full representation round trips without defining and implementing a state format. NetworkX/pickle behavior would not by itself constitute a stable public serialization contract. |
| Representation invariants | Partial | Constructors reject nonsimple base graphs; decomposition scaffolds preserve base graphs and materialize induced subgraphs; several operator docstrings state local invariants. | There is no central `validate()` function and no uniform postcondition check. Mapping validity, identity consistency, provenance completeness, determinism, composition closure, and state round-trip preservation remain open obligations. |
| Complexity analysis | Partial | Many operator docstrings contain local time/memory notes; hashing documentation estimates rooted hashing near `O(|V|(|V|+|E|))` plus tie-dependent canonical search. | The notes are not normalized or validated, 38 complexity headings do not cover the full 54-operator registry, and no manuscript-ready table or empirical scaling evidence exists. |
| Synthetic data support | Partial | `artificial.py` provides random graph and dataset constructors. | The proposed `SYN-PERM-01` and `SYN-SCALE-01` datasets are not frozen, versioned, or checksummed, and their expected invariances are not specified. |
| Correctness tests | Partial and unverified | `tests/test_canonical_terminology.py` contains 39 tests for terminology, mapped-subgraph helpers, representative operators, directed behavior, hashing, scaffold metadata, and selected XML round trips. `scripts/smoke_test.py` exercises a minimal graph-to-vector path. | The test suite could not be run because the active Python environment does not contain `pytest`. `pyproject.toml` declares no test/development dependency group or test configuration. |
| Permutation-invariance tests | Partial | Tests compare graph hashes before and after selected node relabelings in fast and canonical modes. | No property-based or generated suite tests complete decompositions, interpretation-graph isomorphism, attribute ordering, all identity modes, or operator programs across seeds. |
| Identity collision/stability experiments | Missing | Bounded hash widths are configurable and documentation acknowledges collision risk. | No collision corpus, expected-rate calculation, cross-process/platform stability run, or collision resolution policy was found. |
| Scaling benchmarks | Missing | Parallel conversion and hashing helpers exist, and some docstrings discuss complexity. | No benchmark entry point records graph size, density, program depth, runtime, or peak memory using the Paper 1 manifest schema. |
| Baseline representations | Missing | Graphlet-like decomposition exists as an AbstractGraph operator. | No independent WL, graphlet, motif-counting, or graph-grammar baseline implementation/configuration is selected in the benchmark registry. |

## Implemented object model

The implementation most closely corresponds to

\[
A=(G,I,\mu,\ell,a,r),
\]

where `G` is a simple NetworkX base graph, `I` is a simple undirected NetworkX
interpretation graph, and `mu(v)` is stored by value as the `mapped_subgraph`
attribute of interpretation node `v`. The implementation also carries
pluggable interpretation-node label and attribute functions (`ell` and `a`)
and an interpretation-edge function `r`. These functions are configuration on
the Python object rather than fields with a serialization or equality contract.

This differs from the current manuscript notation `A=(G,I,mu)`. The formalism
must decide whether the functions are part of the mathematical object, part of
an execution environment, or parameters of an update operation.

## Operator surface

The 54 registered operators fall into these implementation categories:

- four higher-order composition operators;
- four conditional or iterative operators;
- decomposition operators over nodes, edges, components, neighborhoods, paths,
  cycles, graphlets, cliques, partitions, and centrality;
- transforms and set-like operations such as complements, merge,
  deduplication, intersection, and combinations;
- structural and label filters;
- binary combination/intersection, relabeling, and naming operations.

Scalar reducers exist outside the XML operator registry. For Paper 1, the
reference suite should be explicitly selected from the registry and assigned a
contract row containing input conditions, output semantics, directedness,
determinism, provenance behavior, and asymptotic cost.

## Claim-to-implementation map

| Claim ID | Current support | Current evidence | Missing before claim can advance |
| --- | --- | --- | --- |
| P1-C1: mapped decompositions preserve links to base structure | Partial | Mapped subgraphs retain base identifiers; helper and representative scaffold tests inspect mappings and parent metadata. | Freeze mapping rules; implement validation; define edge provenance; test provenance completeness for every reference operator and compositions. |
| P1-C2: operator programs form a compositional language | Partial | Four composition forms, control flow, XML operator trees, directed-support metadata, and selected composition/XML tests exist. | Define typed semantics and closure; select the normative operator subset; test behavioral XML equivalence and failure contracts; state which algebraic laws do and do not hold. |
| P1-C3: components receive stable identities under a declared equivalence | Partial | Deterministic bounded hashing, fast/canonical modes, and selected relabeling tests exist. | Declare equivalence and attribute rules; separate canonical certificate from bounded feature ID; specify collisions; run stability and collision experiments. |
| P1-C4: decomposition and identity are invariant to node permutation | Weak partial | Selected graph-hash relabeling examples exist. | Generate permutations across graph families and attributes; compare full mapped decompositions and interpretation graphs; cover deterministic reference operators and state exclusions for random operators. |
| P1-C5: scaling and expressiveness are characterized | Missing evidence | Local complexity notes and a broad operator implementation exist. | Build benchmark pipeline, freeze synthetic families, select baselines, record runtime/memory, and run expressiveness and scaling pilots. |

All five claims should remain `Proposed` in the shared claim ledger. The
implementation is promising, but the present artifacts do not yet justify
`Specified` because the formal contracts and evidence links are incomplete.

## Priority gaps

1. **Freeze the supported object model.** Decide induced versus edge-induced
   mappings, empty/disconnected/overlapping mappings, attribute equivalence,
   directedness, and whether configuration functions belong to `A`.
2. **Add representation validation.** A central validator should check graph
   class, mapping membership, preserved node/edge data, interpretation payloads,
   and declared provenance requirements.
3. **Define the provenance model.** Prefer normalized base-node/base-edge sets
   and derivation records over copied parent graphs; specify how provenance
   composes.
4. **Separate canonical identity from bounded feature hashing.** Define the
   equivalence certificate, feature-ID reduction, collision detection, and
   collision handling as distinct layers.
5. **Specify and serialize full Abstract Graph states.** Operator XML alone is
   insufficient for the planned serialization-cycle claim.
6. **Select a normative reference operator subset.** Give every selected
   operator a typed contract, invariant tests, provenance tests, and complexity
   entry before expanding coverage.
7. **Create executable evidence infrastructure.** Declare test dependencies,
   add property-based permutation tests, and implement smoke-sized scaling and
   round-trip experiment entry points using the manifest metadata schema.

## Recommended next artifact

Use this inventory to revise `formalism.md` into a frozen decision document.
The first decision pass should resolve the supported graph class, mapping
validity predicate, equivalence/identity layers, provenance record, and the
status of label/attribute/edge functions. Those decisions unblock both the
reference-operator contracts and scientific experiments E01 and E02.

## Verification record

- Source and documentation were inspected at the revision and worktree state
  recorded above.
- The repository contains 39 discovered `test_` functions in one test module.
- `python -m pytest -q` was attempted from `repos/abstractgraph` and could not
  start because `pytest` is not installed in the active Python environment.
- No source files inside `repos/abstractgraph` were changed by this audit.
