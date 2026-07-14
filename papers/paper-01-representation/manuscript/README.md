# LaTeX manuscript

The paper uses the standard LaTeX `article` class so that the source can be
uploaded to arXiv without a journal-specific class. Each manuscript section is
kept in `sections/` and assembled by `main.tex`.

Build from this directory with:

```sh
latexmk -pdf main.tex
```

Remove generated build files with:

```sh
latexmk -C main.tex
```

Before submission, replace the placeholder author line, populate the shared
bibliography, and copy all required sources (including the shared `.bib` file
and generated figures) into the arXiv upload bundle while preserving their
relative paths or updating the paths in `main.tex`.
