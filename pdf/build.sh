#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Backup originálu při prvním spuštění (s ochranou proti zachycení už-prependnutého stavu)
EXPECTED_ORIG_PAGES=18
if [ ! -f merged_orig.pdf ]; then
  CURRENT_PAGES=$(pdfinfo merged.pdf | awk '/^Pages/ {print $2}')
  if [ "$CURRENT_PAGES" -ne "$EXPECTED_ORIG_PAGES" ]; then
    echo "ERROR: merged.pdf má ${CURRENT_PAGES} stran (očekáváno ${EXPECTED_ORIG_PAGES})." >&2
    echo "Backup merged_orig.pdf chybí a aktuální merged.pdf už není originál — obnov 18-stránkovou verzi a spusť znovu." >&2
    exit 1
  fi
  cp merged.pdf merged_orig.pdf
fi

# Build titulky
pdflatex -interaction=nonstopmode titlepage.tex >/dev/null 2>&1 || { tail -30 titlepage.log >&2; echo "pdflatex failed; see titlepage.log" >&2; exit 1; }

# Merge titulka + originál → přepsat merged.pdf
pdfunite titlepage.pdf merged_orig.pdf merged.pdf

PAGES=$(pdfinfo merged.pdf | awk '/^Pages/ {print $2}')
echo "Done. merged.pdf = titlepage + merged_orig.pdf (${PAGES} stran)"
