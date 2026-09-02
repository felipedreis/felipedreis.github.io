#!/usr/bin/env python3
"""Generate a LaTeX CV (and PDF) from _data/cv.yml.

Local-only tool: it is not part of the Jekyll build and its output is not
committed to the repo (see .gitignore). Run it whenever _data/cv.yml changes.

Usage:
    python3 cv-builder/build_cv.py            # writes cv.tex and cv.pdf
    python3 cv-builder/build_cv.py --no-pdf    # only writes cv.tex

Requires PyYAML and Jinja2 (see requirements.txt). Producing the PDF also
requires a LaTeX toolchain on PATH: latexmk, tectonic, or pdflatex -- e.g. on
macOS, `brew install --cask basictex` (or `mactex` for the full distribution).
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent
BUILDER_DIR = Path(__file__).resolve().parent
DATA_FILE = ROOT / "_data" / "cv.yml"
DEFAULT_OUTPUT_DIR = BUILDER_DIR / "output"

# Characters LaTeX treats specially; escaped when injecting plain text pulled
# from YAML so the source stays valid regardless of what's typed in cv.yml.
LATEX_SPECIAL_CHARS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}
LATEX_SPECIAL_RE = re.compile("|".join(re.escape(k) for k in LATEX_SPECIAL_CHARS))


def escape_tex(value):
    """Escape LaTeX special characters in a plain-text YAML value."""
    if value is None:
        return ""
    text = str(value).strip()
    return LATEX_SPECIAL_RE.sub(lambda m: LATEX_SPECIAL_CHARS[m.group()], text)


def tex_paragraphs(value):
    """Escape a multi-line YAML block, preserving blank-line paragraph breaks."""
    text = escape_tex(value)
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    return "\n\n".join(parts) if parts else text


def load_cv_data():
    if not DATA_FILE.exists():
        sys.exit(f"Could not find CV data at {DATA_FILE}")
    with DATA_FILE.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_jinja_env():
    # LaTeX and Jinja2 both lean on `{` `}` and `%`, so use the standard
    # LaTeX-friendly delimiter set instead of Jinja2's defaults.
    env = Environment(
        loader=FileSystemLoader(str(BUILDER_DIR)),
        block_start_string=r"\BLOCK{",
        block_end_string="}",
        variable_start_string=r"\VAR{",
        variable_end_string="}",
        comment_start_string=r"\#{",
        comment_end_string="}",
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
    )
    env.filters["tex"] = escape_tex
    env.filters["texpar"] = tex_paragraphs
    return env


def find_latex_compiler():
    for candidate in ("latexmk", "tectonic", "pdflatex"):
        if shutil.which(candidate):
            return candidate
    return None


def compile_pdf(tex_path: Path, output_dir: Path):
    compiler = find_latex_compiler()
    if not compiler:
        print(
            "No LaTeX compiler found (looked for latexmk, tectonic, pdflatex) -- "
            "skipping PDF generation. Install a TeX distribution, e.g. on macOS: "
            "`brew install --cask basictex`, then re-run this script.",
            file=sys.stderr,
        )
        return None

    if compiler == "latexmk":
        cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
               f"-output-directory={output_dir}", str(tex_path)]
        passes = 1
    elif compiler == "tectonic":
        cmd = ["tectonic", "--outdir", str(output_dir), str(tex_path)]
        passes = 1
    else:  # pdflatex: run twice, harmless today and future-proofs any refs/TOC
        cmd = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
               f"-output-directory={output_dir}", str(tex_path)]
        passes = 2

    for _ in range(passes):
        result = subprocess.run(cmd, cwd=output_dir, capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stdout[-4000:], file=sys.stderr)
            print(result.stderr[-2000:], file=sys.stderr)
            sys.exit(f"{compiler} failed to compile {tex_path.name}")

    pdf_path = output_dir / (tex_path.stem + ".pdf")
    return pdf_path if pdf_path.exists() else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--no-pdf", action="store_true", help="only generate the .tex file")
    args = parser.parse_args()

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    cv = load_cv_data()
    env = build_jinja_env()
    tex_source = env.get_template("template.tex.j2").render(cv=cv)

    tex_path = output_dir / "cv.tex"
    tex_path.write_text(tex_source, encoding="utf-8")
    print(f"Wrote {tex_path.relative_to(ROOT)}")

    if not args.no_pdf:
        pdf_path = compile_pdf(tex_path, output_dir)
        if pdf_path:
            print(f"Wrote {pdf_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
