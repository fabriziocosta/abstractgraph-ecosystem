# AbstractGraph Ecosystem

This repository is the container superproject for the main AbstractGraph
repositories, managed as Git submodules under `repos/`.

Included repositories:

- `repos/abstractgraph`
  Role: core representation, operators, XML, hashing, vectorization, display,
  compatibility shims, and graph adapters

- `repos/abstractgraph-graphicalizer`
  Role: raw-data-to-NetworkX graphicalizers, including attention-driven
  base-graph induction and chemistry conversion/drawing

- `repos/abstractgraph-ml`
  Role: estimators, neural models, feasibility, importance, and top-k analysis

- `repos/abstractgraph-generative`
  Role: rewriting, autoregressive and conditional generation, interpolation,
  optimization/repair, and story-graph tooling

Dependency direction:

- `abstractgraph`
- `abstractgraph-graphicalizer` depends on no sibling repos
- `abstractgraph-ml` depends on `abstractgraph`
- `abstractgraph-generative` depends on `abstractgraph` and `abstractgraph-ml`

Editable install order from this superproject checkout:

```bash
python -m pip install -e repos/abstractgraph --no-deps
python -m pip install -e repos/abstractgraph-graphicalizer --no-deps
python -m pip install -e repos/abstractgraph-ml --no-deps
python -m pip install -e repos/abstractgraph-generative --no-deps
```

## Submodule Workflow

Each child repository remains an independent Git repository. Changes to the
ecosystem may require work in one or more submodules plus a parent commit that
updates the pinned submodule SHAs.

Typical sequence:

```bash
git -C repos/abstractgraph status
git -C repos/abstractgraph add -A
git -C repos/abstractgraph commit -m "Your message"
git -C repos/abstractgraph push origin main

git -C repos/abstractgraph-ml status
git -C repos/abstractgraph-ml add -A
git -C repos/abstractgraph-ml commit -m "Your message"
git -C repos/abstractgraph-ml push origin main

git add repos/abstractgraph repos/abstractgraph-ml
git commit -m "Update submodule pointers"
git push origin main
```

When only one child repository changes, only add that submodule path in the
parent commit.

## Repo-Sync Rule

When one logical change spans multiple child repositories:

- commit each child repo separately
- push each child repo separately
- update the superproject submodule pointers afterward
- verify `git status` is clean in each touched repo and in the superproject
