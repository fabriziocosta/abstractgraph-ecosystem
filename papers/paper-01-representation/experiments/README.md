# Paper 1 Experiments

`manifest.yaml` is the authoritative experiment index. Each run must use a
versioned configuration from `configs/` and emit the metadata listed in the
manifest.

The experiment programme has three tracks: prerequisite representation
validation, RQ1 structural discrimination, and RQ2 discrimination--complexity.
Pooling, predictive probes, and identity collisions are analyses within RQ1,
not separate research questions.

## Workflow

1. Specify the hypothesis, dataset, baseline, metric, and expected artifact.
2. Validate the experiment with a smoke-sized configuration.
3. Freeze the configuration before confirmatory runs.
4. Write raw outputs under `../results/` using a unique run ID.
5. Generate tables and figures through code recorded under `../analysis/`.
6. Link accepted evidence in `../../shared/claim-ledger.md`.

Do not place exploratory and confirmatory results under the same run series.
