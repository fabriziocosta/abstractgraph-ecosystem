# Analysis

Place scripts or notebooks that transform immutable raw results into statistics,
tables, and figures here. Analysis must not modify raw results. Each output must
record its input run IDs and analysis code revision.

Prefer scripts for final analysis. Exploratory notebooks must be converted into
repeatable entry points before their outputs are used in the manuscript.

## Research-question notebooks

`notebooks/` contains one validation notebook and one orchestration notebook per
research question:

- `validation.ipynb`: traceability, serialization, and invariance;
- `RQ1-structural-discrimination.ipynb`: intrinsic discrimination, probes,
  pooling, reserved-feature controls, and hash collisions;
- `RQ2-discrimination-complexity.ipynb`: runtime, memory, representation size,
  and Pareto analysis.

Each notebook must:

1. load its versioned configuration from `../experiments/configs/`;
2. state the criterion that would answer the research question;
3. generate or load immutable raw data under `../results/<experiment>/<run>/`;
4. call reusable experiment and analysis functions rather than define them in
   notebook cells;
5. generate the declared tables and figures under `../tables/generated/` and
   `../figures/generated/`; and
6. be saved as `executed-notebook.ipynb` in the run directory.

Shared provenance and export behavior lives in `notebook_support.py`. A
confirmatory notebook is complete only when it runs from a clean checkout with
a frozen configuration and no manual cell edits.
