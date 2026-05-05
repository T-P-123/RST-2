#!/usr/bin/env python3
"""
Build the unified report by:
1. Compiling cover.tex -> cover.pdf (title page + TOC)
2. Concatenating cover.pdf + 5 original example PDFs (byte-perfect copy)
3. Adding PDF outline (bookmarks) for navigation
4. Writing reseni_E.pdf
"""

import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).parent
ORIG = ROOT / "orig_pdfs"


def compile_cover() -> Path:
    """Compile cover.tex twice (TOC stable)."""
    for _ in range(2):
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "cover.tex"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            sys.stderr.write(result.stdout[-2000:])
            raise SystemExit("pdflatex cover.tex failed")
    return ROOT / "cover.pdf"


def merge() -> Path:
    cover = compile_cover()
    examples = [
        ("Příklad 1E -- Stochastické vyhodnocení vnitřních účinků nosníku", ORIG / "priklad1E.pdf"),
        ("Příklad 2E -- Osový kvadratický moment nesymetrického průřezu", ORIG / "priklad2E.pdf"),
        ("Příklad 3E -- Výpočet pravděpodobnosti bezporuchového provozu", ORIG / "priklad3E.pdf"),
        ("Příklad 4E -- MS pružnosti a deformace stupňovitého prutu", ORIG / "priklad4E.pdf"),
        ("Příklad 5E -- Časový průběh napětí ve vrubech", ORIG / "priklad5E.pdf"),
    ]

    writer = PdfWriter()

    # 1) Cover (title page + TOC) - 2 pages
    cover_reader = PdfReader(cover)
    for page in cover_reader.pages:
        writer.add_page(page)

    # 2) Add bookmark for cover
    writer.add_outline_item("Titulní strana", page_number=0)
    writer.add_outline_item("Obsah", page_number=1)

    # 3) Append each example PDF (byte-perfect page copy) + bookmark
    page_offset = len(cover_reader.pages)
    for title, pdf_path in examples:
        reader = PdfReader(pdf_path)
        first_page = page_offset
        for page in reader.pages:
            writer.add_page(page)
        writer.add_outline_item(title, page_number=first_page)
        page_offset += len(reader.pages)

    out = ROOT / "reseni_E.pdf"
    with open(out, "wb") as f:
        writer.write(f)
    print(f"Wrote {out}, total {page_offset} pages.")
    return out


if __name__ == "__main__":
    merge()
