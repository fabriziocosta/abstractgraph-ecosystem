# Ecosystem Organization

`abstractgraph-ecosystem` is a Git superproject that brings together the main
AbstractGraph repositories as Git submodules under `repos/`.

For the semantic role of each repository and how the layers work together, see
[../README.md](../README.md).

## Included Repositories

- `repos/abstractgraph`
- `repos/abstractgraph-generative`
- `repos/abstractgraph-graphicalizer`
- `repos/abstractgraph-ml`

## Clone

Clone the superproject and all submodules in one step:

```bash
git clone --recurse-submodules git@github.com:fabriziocosta/abstractgraph-ecosystem.git
```

If you already cloned the superproject without submodules, initialise them
afterwards with:

```bash
git submodule update --init --recursive
```

## Dependency Direction

- `abstractgraph`
- `abstractgraph-graphicalizer` depends on no sibling repositories
- `abstractgraph-ml` depends on `abstractgraph`
- `abstractgraph-generative` depends on `abstractgraph` and `abstractgraph-ml`

## Editable Install Order

From this superproject checkout:

```bash
python -m pip install -e repos/abstractgraph --no-deps
python -m pip install -e repos/abstractgraph-graphicalizer --no-deps
python -m pip install -e repos/abstractgraph-ml --no-deps
python -m pip install -e repos/abstractgraph-generative --no-deps
```

## Submodule Pinning

Each submodule is pinned to a specific commit in the parent repository. Updating
a child repository is a two-step operation:

1. Move the submodule checkout to the desired commit.
2. Commit the updated submodule pointer in this parent repository.

Example:

```bash
cd repos/abstractgraph-ml
git fetch origin
git checkout <new-commit-or-branch>
cd ../..
git add repos/abstractgraph-ml
git commit -m "Update abstractgraph-ml submodule"
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

This keeps each package independently usable while still allowing this
superproject to pin compatible cross-repository states.

## Create the Superproject

The superproject was created with:

```bash
git init
git branch -m main
git submodule add https://github.com/fabriziocosta/abstractgraph.git repos/abstractgraph
git submodule add https://github.com/fabriziocosta/abstractgraph-generative.git repos/abstractgraph-generative
git submodule add https://github.com/fabriziocosta/abstractgraph-graphicalizer.git repos/abstractgraph-graphicalizer
git submodule add https://github.com/fabriziocosta/abstractgraph-ml.git repos/abstractgraph-ml
git add .gitmodules repos README.md
git commit -m "Initialise abstractgraph ecosystem superproject"
```
