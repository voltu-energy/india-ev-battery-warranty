#!/usr/bin/env python3
"""Validate the dataset. Run before every commit and in CI.

The one rule this enforces: every value that is not an explicit absence must be traceable to a
source document with a date it was read. A cell with a value and no source is the defect this
dataset exists to avoid.
"""
import csv, json, re, sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data"
ABSENCES = {"NOT_FOUND", "NOT_STATED", "NOT_DISCLOSED", "NOT_ADDRESSED", "NO_FIGURE_IN_DOCUMENT",
             "PARTIAL", "DISCLOSED",
             # 1.1.0. Stronger than NOT_STATED and the opposite of a gap: the document addresses this
             # and puts it outside cover. BYD excludes normal capacity attenuation in terms.
             "EXCLUDED"}
DOC_TYPES = {"owner_manual_pdf", "warranty_booklet_pdf", "official_warranty_page",
             "official_model_page", "brochure_pdf", "press_release",
             # 1.1.0. A maker that publishes nothing is a result, and a result needs a record.
             # official_faq_page: the maker's own FAQ is the only page that addresses the battery.
             # none_located: the URL was reached and serves no warranty document. access_notes must
             # say how that was established, including any browser pass.
             "official_faq_page", "none_located"}
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
by_id = {s["source_id"]: s for s in sources}
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
    # THE RULE: a stated value needs a source document. An absence is always allowed.
    #
    # 1.1.0: this check used to test `not r["source_id"]`, which the unknown-source_id check above
    # already catches, so it could never fire. It now tests what the rule actually means: the cited
    # source must be a document. A real figure resting on a none_located record would be a value with
    # nothing behind it, which is the one defect this dataset cannot carry.
    src = by_id.get(r["source_id"])
    for field in ("warranty_years", "warranty_km", "soh_floor_pct", "who_measures"):
        v = r[field].strip()
        if v and v not in ABSENCES:
            if not r["source_id"]:
                errors.append(f"warranty-terms.csv line {i}: {field} has a value with no source_id")
            elif src and src["document_type"] == "none_located":
                errors.append(f"warranty-terms.csv line {i}: {field} states '{v}' but its source "
                              f"{r['source_id']} is a none_located record, so nothing supports it")
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

# THE DENOMINATOR GUARD, added 1 October 2026.
#
# A clause scope reads "5 of 7 manuals". Then the XPRES-T EV manual was found and read, the real
# denominator became eight, and three scopes in clauses.csv, three in warranty.json and three lines of
# the README went on saying seven for two days. A fraction whose numerator is checked and whose
# denominator is typed is the exact defect this repository exists to rule out, so it is checked here.
#
# Rule: in any clause scope of the form "N of M", M must equal the number of owner-manual documents
# this dataset holds for that clause's maker. If a manual is added and a scope is not revisited, this
# fails.
manuals_by_maker = {}
for srow in sources:
    if srow["document_type"] == "owner_manual_pdf":
        manuals_by_maker[srow["maker"]] = manuals_by_maker.get(srow["maker"], 0) + 1

FRACTION = re.compile(r"\b(\d+)\s+of\s+(\d+)\b")
for i, c in enumerate(clauses, 2):
    expected = manuals_by_maker.get(c["maker"])
    for num, den in FRACTION.findall(c["model_scope"]):
        if expected is None:
            errors.append(f"clauses.csv line {i}: scope says '{num} of {den}' but no owner manual "
                          f"is recorded for {c['maker']}, so the denominator rests on nothing")
        elif int(den) != expected:
            errors.append(f"clauses.csv line {i}: scope says '{num} of {den}' but sources.csv holds "
                          f"{expected} owner manuals for {c['maker']}")
        elif int(num) > expected:
            errors.append(f"clauses.csv line {i}: scope says '{num} of {den}', and {num} is more "
                          f"manuals than exist")

# The same denominators are written out in prose. Catch the word forms too.
#
# The prose does not always name the maker in the same clause ("Its eight EV owner manuals are not
# uniform"), so look back a little for a maker name, and fall back to the only maker that has manuals
# when there is exactly one.
WORDS = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
         "ten": 10, "eleven": 11, "twelve": 12}
PROSE = re.compile(r"(\w+)\s+EV owner manuals", re.IGNORECASE)
for doc in ("README.md", "CHANGELOG.md"):
    try:
        text = open(doc, encoding="utf-8").read()
    except OSError:
        continue
    for m in PROSE.finditer(text):
        den = WORDS.get(m.group(1).lower())
        if den is None:
            continue
        back = text[max(0, m.start() - 160):m.start()]
        named = [mk for mk in manuals_by_maker if mk.split()[0].lower() in back.lower()]
        if named:
            expected = manuals_by_maker[named[-1]]
            who = named[-1]
        elif len(manuals_by_maker) == 1:
            who, expected = next(iter(manuals_by_maker.items()))
        else:
            continue
        if den != expected:
            errors.append(f"{doc}: '{m.group(0)}' but sources.csv holds {expected} owner manuals "
                          f"for {who}")

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
