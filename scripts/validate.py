#!/usr/bin/env python3
"""Validate the dataset. Run before every commit and in CI.

The one rule this enforces: every value that is not an explicit absence must be traceable to a
source document with a date it was read. A cell with a value and no source is the defect this
dataset exists to avoid.
"""
import csv, json, re, sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data"
ABSENCES = {"NOT_FOUND", "NOT_STATED", "NOT_DISCLOSED", "NOT_ADDRESSED", "NO_FIGURE_IN_DOCUMENT", "PARTIAL", "DISCLOSED"}
DOC_TYPES = {"owner_manual_pdf", "warranty_booklet_pdf", "official_warranty_page",
             "official_model_page", "brochure_pdf", "press_release"}
SEGMENTS = {"2W", "3W", "4W"}
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def read(name):
    with open(D / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))

errors, warnings = [], []

sources = read("sources.csv")
terms = read("warranty-terms.csv")
clauses = read("clauses.csv")

ids = {s["source_id"] for s in sources}
if len(ids) != len(sources):
    errors.append("sources.csv: duplicate source_id")

for s in sources:
    if not ISO.match(s["date_read"]):
        errors.append(f"sources.csv: {s['source_id']} date_read is not ISO 8601: {s['date_read']}")
    if s["document_type"] not in DOC_TYPES:
        errors.append(f"sources.csv: {s['source_id']} unknown document_type: {s['document_type']}")
    if not s["url"].startswith("https://"):
        errors.append(f"sources.csv: {s['source_id']} url is not https")

for i, r in enumerate(terms, 2):
    if r["source_id"] not in ids:
        errors.append(f"warranty-terms.csv line {i}: unknown source_id {r['source_id']}")
    if r["segment"] not in SEGMENTS:
        errors.append(f"warranty-terms.csv line {i}: unknown segment {r['segment']}")
    # THE RULE: a stated value needs a source. An absence is always allowed.
    for field in ("warranty_years", "warranty_km", "soh_floor_pct", "who_measures"):
        v = r[field].strip()
        if v and v not in ABSENCES and not r["source_id"]:
            errors.append(f"warranty-terms.csv line {i}: {field} has a value with no source_id")
    if not r["maker"] or not r["model"]:
        errors.append(f"warranty-terms.csv line {i}: maker and model are required")

for i, c in enumerate(clauses, 2):
    if c["source_id"] not in ids:
        errors.append(f"clauses.csv line {i}: unknown source_id {c['source_id']}")
    if len(c["clause_text"].strip()) < 10:
        errors.append(f"clauses.csv line {i}: clause_text looks empty or truncated")
    if not c["model_scope"].strip():
        errors.append(f"clauses.csv line {i}: model_scope is required; a clause with no scope is how "
                      f"'five of seven manuals' becomes 'the maker'")

unused = ids - {r["source_id"] for r in terms} - {c["source_id"] for c in clauses}
for u in sorted(unused):
    warnings.append(f"sources.csv: {u} is not referenced by any row")

for w in warnings:
    print(f"warning: {w}")
for e in errors:
    print(f"ERROR: {e}")

print(f"\n{len(sources)} sources, {len(terms)} models, {len(clauses)} clauses")
print(f"{len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
