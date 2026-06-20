#!/usr/bin/env python3
"""T1 build step - ZERO tokens. Renders each tree-JSON fixture into a standalone HTML
by swapping the data block of assets/tree-template.html. Then open tests/out/*.html.
  run:  python3 tests/build_fixtures.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "tree-template.html"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
FIXTURES = sorted((HERE / "fixtures").glob("*.json"))
# also render any tree-JSON dropped in out/ (plumbing.test.mjs output, smoke-workflow output, etc.)
GENERATED = sorted(OUT.glob("*.json"))

tpl = TEMPLATE.read_text()
DATA_RE = re.compile(
    r'(<script id="tree-data" type="application/json">)(.*?)(</script>)', re.DOTALL
)

def build(name: str, data_json: str):
    # validate it's parseable JSON before injecting
    json.loads(data_json)
    html = DATA_RE.sub(lambda m: m.group(1) + "\n" + data_json.strip() + "\n" + m.group(3), tpl)
    out = OUT / f"{name}.html"
    out.write_text(html)
    print(f"  built  {out.relative_to(HERE.parent)}")

print("--- T1 render build ---")
sources = list(FIXTURES) + list(GENERATED)
if not sources:
    print("  no fixtures found")
for f in sources:
    build(f.stem, f.read_text())
print(f"\nOpen tests/out/*.html in a browser (or serve the skill dir).")
