# Cycle--path--star discrimination benchmark

Dataset ID: `SYN-CPS-01`

Experiment family: `E03-expressiveness`

## Objective

Measure which controlled structural distinctions are retained by an operator
program or adjacent graph representation. This is a representation experiment,
not a predictive benchmark: dataset labels and fitted classifiers are not part
of the primary result.

## Generator

Use `abstractgraph.artificial.generate_artificial_dataset`. A generated unit
contains zero or more edge-sharing cycles, a path, and zero or more rays joined
at a star hub. Units can be attached recursively to ray endpoints. Nodes and
edges record both their sampled labels and the component that produced them;
graph metadata records every sampled structural parameter.

The default pilot grid is:

| Factor | Values |
| --- | --- |
| Cycle length | 0, 3, 4, 5, 6 |
| Number of cycles | 0, 1, 2 |
| Path length | 0, 1, 2, 4 |
| Number of rays | 0, 1, 2, 4 |
| Ray length | 0, 1, 2, 3 |
| Iteration depth | 1, 2, 3 |
| Node alphabet size | 1, 2, 4 |
| Edge alphabet size | 1, 2 |
| Alphabet allocation | shared, component-specific |

Invalid combinations, including an entirely empty unit, are excluded before
sampling. The confirmatory grid and sample count will be frozen after a
smoke-sized pilot establishes runtime bounds.

## Pair construction

For each seed, construct:

1. an original graph \(G\);
2. identifier-permuted copies \(\rho(G)\);
3. attribute-order perturbations that preserve semantic attributes; and
4. matched graphs \(G_f\) in which exactly one structural factor \(f\) changes.

Pairs \((G,\rho(G))\) are equivalent controls and must receive equivalent
representations. A pair \((G,G_f)\) is a discrimination target only after an
exact attributed-isomorphism check confirms that it is non-equivalent under the
declared attribute projection.

## Representation signature

Every method must emit a deterministic comparison signature containing its
multiset of structural feature identities and, where available, the typed
interpretation relations between them. Record the identity projection, hash
width, collision policy, and operator-program serialization with every
signature.

## Primary metrics

- **Invariant agreement:** fraction of equivalent control pairs receiving
  equivalent signatures; target 1.0 for deterministic methods.
- **One-factor discrimination rate:** fraction of verified non-equivalent
  matched pairs receiving distinct signatures, reported separately by factor.
- **Unique-signature ratio:** number of distinct signatures divided by the
  number of non-isomorphic attributed graphs.
- **Representation collision count:** non-isomorphic graphs sharing a
  signature, with bounded-hash collisions reported separately from method
  indistinguishability.
- **Resolution curve:** discrimination rate as operator-program depth or method
  refinement depth increases.

Secondary outcomes are signature size, representation time, and peak memory.
No single aggregate score may hide factor-specific failures.

## Methods

The primary comparison will include predeclared AbstractGraph operator programs
at increasing depth. Adjacent baselines are Weisfeiler--Lehman refinement,
graphlet counts, and motif counts. A graph-grammar comparison remains optional
until a representation with comparable input assumptions and output semantics
is selected.

## Reproducibility

Each run records the generator version, complete configuration, dataset and
graph seeds, actual per-unit draws, graph hashes before representation,
operator-program serialization, method version, and raw pair-level outcomes.
Generated graphs are immutable once the confirmatory manifest is frozen.
