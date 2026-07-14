# Dataset Registry

No dataset is approved for final experiments until its licence, immutable
version, processing, graph construction, and split are recorded here.

| Dataset ID | Domain | Source/version | Licence | Graph construction | Task | Split artifact | Papers | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SYN-CPS-01 | Synthetic | `abstractgraph.artificial.generate_artificial_dataset`, schema version 1 | Project-generated | Parameterised cycle--path--star compositions with ground-truth component metadata | Default controlled study of representation discrimination and operator-program expressiveness | Seed/config manifest to create | 1--5 | Selected |
| SYN-PERM-01 | Synthetic | SYN-CPS-01 plus identifier and attribute-order perturbations | Project-generated | Relabelled copies of frozen cycle--path--star instances | Permutation invariance and identity stability | Permutation manifest to create | 1 | Selected |
| SYN-SCALE-01 | Synthetic | SYN-CPS-01 plus simple random graph families | Project-generated | Factorial variation of graph size, density, alphabet size, and program depth | Runtime and memory scaling | Scaling manifest to create | 1 | Selected |
| OGB-MOLHIV-CAND | Molecules | [`ogbg-molhiv`, OGB package >=1.1.1](https://ogb.stanford.edu/docs/graphprop/) | MIT | Molecules represented as atom/bond graphs with OGB atom and bond features | Real-world structural diversity and runtime validation; predictive labels are out of scope for Paper 1 | Official scaffold split; immutable local instance manifest required | 1--3 | Candidate |
| OGB-PPA-CAND | Protein association networks | [`ogbg-ppa`, OGB package >=1.1.1](https://ogb.stanford.edu/docs/graphprop/) | CC0 | Undirected protein-association neighborhoods with seven-dimensional edge features | Non-molecular topology, density, and scaling validation; predictive labels are out of scope for Paper 1 | Official species split; predeclared stratified subset permitted for Paper 1 compute | 1--3, 7 | Candidate |

## Default synthetic family: SYN-CPS-01

SYN-CPS-01 is the default synthetic generator for representation experiments.
It constructs connected graphs from controlled cycle, path, and star/ray units.
Each structural parameter may be fixed or sampled from an inclusive integer
range:

- cycle length and number of edge-sharing cycles;
- path length;
- number and length of rays;
- iterative composition depth;
- node- and edge-label alphabet size; and
- shared versus component-specific alphabets.

Every graph stores the actual per-unit parameter draws, component labels,
structural roles, dataset seed, graph index, and graph seed. This makes it
possible to vary one structural factor at a time, recover the known source of a
difference, and test whether a representation distinguishes that difference.
The matching plotter uses stable red/blue/green palettes for cycle, path, and
star labels.

The Paper 1 default task is **pair discrimination**, not supervised graph
classification. Given a base configuration and a one-factor structural
perturbation, a method succeeds when it assigns different representation
signatures to non-equivalent graphs while remaining invariant to identifier
permutations of the same graph.

The generator implementation and tests live in:

- `repos/abstractgraph/src/abstractgraph/artificial.py`
- `repos/abstractgraph/tests/test_artificial.py`

The frozen experimental design is documented in
[`../paper-01-representation/experiments/cycle-path-star.md`](../paper-01-representation/experiments/cycle-path-star.md).

## Real-world selection gate

`OGB-MOLHIV-CAND` and `OGB-PPA-CAND` are candidates, not approved final
datasets. They were shortlisted because OGB publishes graph construction,
features, standard splits, package requirements, and explicit licences. Before
promotion to `Selected`, record:

1. the exact OGB and converter versions;
2. raw download checksum and processed-graph manifest;
3. the attribute projection used by each identity method;
4. exclusions and conversion failures;
5. the exact full set or predeclared subset used; and
6. measured feasibility under the Paper 1 compute budget.

MUTAG, PROTEINS, and IMDB-BINARY remain possible sensitivity datasets, but are
not selected because their distributor page does not state a dataset licence.

## Split policy

- Store split membership as an immutable artifact keyed by stable instance ID.
- Reuse the same split whenever a dataset appears in multiple papers.
- Never select methods or hyperparameters using the test split.
- Record exclusions, failed conversions, and duplicate handling.
