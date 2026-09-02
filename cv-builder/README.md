# CV builder (local-only tool)

Generates a plain, human- and AI-readable LaTeX CV (and PDF) from `_data/cv.yml`
— the same data file that drives `/cv/` on the site. Not part of the Jekyll
build; the site never reads anything in this directory.

## Setup

```bash
pip install -r cv-builder/requirements.txt
```

Producing the PDF also requires a LaTeX toolchain on PATH (`latexmk`,
`tectonic`, or `pdflatex`). On macOS: `brew install --cask basictex` (or
`mactex` for the full distribution), then open a new shell so the compiler is
on PATH. Without one, the script still writes the `.tex` source and just
skips the PDF step.

## Usage

```bash
python3 cv-builder/build_cv.py            # writes output/cv.tex and output/cv.pdf
python3 cv-builder/build_cv.py --no-pdf   # only writes output/cv.tex
```

Re-run it any time `_data/cv.yml` changes. Everything under `output/` is
gitignored — regenerate rather than commit it.

## Editing the look

`template.tex.j2` is a normal LaTeX file rendered with Jinja2, using
LaTeX-friendly delimiters so it stays readable as a `.tex` file:
`\VAR{ ... }` for values, `\BLOCK{ ... }` for control flow (`for`/`if`/`set`).
Two custom filters are available: `| tex` escapes plain text for LaTeX, and
`| texpar` does the same while preserving blank-line paragraph breaks.
