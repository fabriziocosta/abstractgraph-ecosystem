# Dataset Registry

No dataset is approved for final experiments until its licence, immutable
version, processing, graph construction, and split are recorded here.

| Dataset ID | Domain | Source/version | Licence | Graph construction | Task | Split artifact | Papers | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SYN-PERM-01 | Synthetic | To define | Project-generated | Parameterised attributed graph generator | Permutation invariance and identity stability | To create | 1 | Proposed |
| SYN-SCALE-01 | Synthetic | To define | Project-generated | Graph families varying size, density, and labels | Runtime and memory scaling | To create | 1 | Proposed |

## Split policy

- Store split membership as an immutable artifact keyed by stable instance ID.
- Reuse the same split whenever a dataset appears in multiple papers.
- Never select methods or hyperparameters using the test split.
- Record exclusions, failed conversions, and duplicate handling.
