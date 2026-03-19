# abstractgraph-ecosystem

`abstractgraph-ecosystem` is a Git superproject that brings together the main AbstractGraph repositories as Git submodules under `repos/`.

Included repositories:

- `repos/abstractgraph`
- `repos/abstractgraph-generative`
- `repos/abstractgraph-graphicalizer`
- `repos/abstractgraph-ml`

## Clone

Clone the superproject and all submodules in one step:

```bash
git clone --recurse-submodules git@github.com:fabriziocosta/abstractgraph-ecosystem.git
```

If you already cloned the superproject without submodules, initialise them afterwards with:

```bash
git submodule update --init --recursive
```

## How submodule pinning works

Each submodule is pinned to a specific commit in the parent repository. Updating a child repository is a two-step operation:

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

## Create the superproject

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
