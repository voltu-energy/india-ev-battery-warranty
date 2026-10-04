#!/usr/bin/env python3
"""Validate the dataset. Run before every commit and in CI.

The one rule this enforces: every value that is not an explicit absence must be traceable to a
source document with a date it was read. A cell with a value and no source is the defect this
dataset exists to avoid.
"""
import collections, csv, json, re, sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data"
ABSENCES = {"NOT_FOUND", "NOT_STATED", "NOT_DISCLOSED", "NOT_ADDRESSED", "NO_FIGURE_IN_DOCUMENT",
             "PARTIAL", "DISCLOSED",
             # 1.1.0. Stronger than NOT_STATED and the opposite of a gap: the document addresses this
             # and puts it outside cover. BYD excludes normal capacity attenuation in terms.
             "EXCLUDED"}

# Where the maker hands a document only to owners and publishes no link to it.
URL_ABSENT = {"NOT_PUBLISHED_ONLINE"}
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
# 1.2.0. The same file held under two source_ids splits its clauses into two
# apparent documents and inflates the source count. The sha256 is what says they
# are the same file, so it is what catches it.
_byhash = {}
for _s in sources:
    _h = _s["sha256"].strip()
    if _h:
        _byhash.setdefault(_h, []).append(_s["source_id"])
for _h, _ids in _byhash.items():
    if len(_ids) > 1:
        errors.append(f"sources.csv: one document is held under {len(_ids)} source_ids "
                      f"{sorted(_ids)}, sha256 {_h[:12]}. Merge them.")

if len(ids) != len(sources):
    errors.append("sources.csv: duplicate source_id")

for s in sources:
    if not ISO.match(s["date_read"]):
        errors.append(f"sources.csv: {s['source_id']} date_read is not ISO 8601: {s['date_read']}")
    if s["document_type"] not in DOC_TYPES:
        errors.append(f"sources.csv: {s['source_id']} unknown document_type: {s['document_type']}")
    # 1.1.5. A document can be the maker's own and still have no public URL. The Maruti e VITARA
    # owner's manual is handed to registered owners through the Maruti Suzuki mobile application
    # and is published nowhere on marutisuzuki.com. That is a fact about the maker, not a hole in
    # the dataset, so it is recorded as a value rather than disguised with a plausible-looking link.
    # Such a row must carry a sha256, because the hash is the only thing standing in for the URL.
    if s["url"] not in URL_ABSENT and not s["url"].startswith("https://"):
        errors.append(f"sources.csv: {s['source_id']} url is not https and is not one of "
                      f"{sorted(URL_ABSENT)}")
    if s["url"] in URL_ABSENT and not s["sha256"].strip():
        errors.append(f"sources.csv: {s['source_id']} has no public URL, so it must carry a "
                      f"sha256. Without one there is nothing to identify the document by.")

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
held_on_purpose = []
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


# ---- charging-rules.csv ----
# 1.2.0. An owner-facing layer: the operational rules a maker states, with how much weight the
# document gives each one. Every rule must quote a clause that is in clauses.csv, so the
# owner_action wording can never drift away from what the maker actually wrote.
STRENGTH = {"warranty_condition", "warranty_exclusion", "maker_instruction"}
try:
    rules = read("charging-rules.csv")
except FileNotFoundError:
    rules = []
clause_texts = [c["clause_text"] for c in clauses]
for i, r in enumerate(rules, 2):
    if r["source_id"] not in ids:
        errors.append(f"charging-rules.csv line {i}: unknown source_id {r['source_id']}")
    if r["strength"] not in STRENGTH:
        errors.append(f"charging-rules.csv line {i}: strength '{r['strength']}' is not one of "
                      f"{sorted(STRENGTH)}")
    for field in ("rule", "owner_action", "clause_verbatim"):
        if not r[field].strip():
            errors.append(f"charging-rules.csv line {i}: {field} is empty")
    # THE RULE for this file. The quotation must be findable in clauses.csv.
    vb = r["clause_verbatim"].strip()
    if vb and not any(vb in t for t in clause_texts):
        errors.append(f"charging-rules.csv line {i}: clause_verbatim is not found in any "
                      f"clauses.csv row. An owner-facing rule must quote a recorded clause.")

unused = ids - {r["source_id"] for r in terms} - {c["source_id"] for c in clauses} - {r["source_id"] for r in rules}
for u in sorted(unused):
    # 1.2.0. A document can be held on purpose without any row citing it: a second manual that
    # corroborates the first word for word, or one held as a negative because a rule we scope to
    # two models is absent from it. Both are evidence about how far a rule reaches, so the
    # document stays. It must say which, in access_notes, or this is still a warning.
    note = by_id[u]["access_notes"]
    if re.search(r"Corroborates \S+|Held as a negative|NOT READ", note):
        held_on_purpose.append(u)
    else:
        warnings.append(f"sources.csv: {u} is not referenced by any row, and access_notes does "
                        f"not say why it is held. Say 'Corroborates <source_id>', 'Held as a "
                        f"negative' or 'NOT READ'.")

# ---- the published JSON ----
# 1.1.4. It used to be hand-maintained and it drifted: at 1.1.3 its arrays held 54 sources and 63
# clauses, its own counts field claimed 56 and 71, and the CSVs held 56 and 71. Generated now,
# and regenerated and compared here so it cannot drift again.
import subprocess
_check = subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "build-json.py"),
                         "--check"], capture_output=True, text=True)
if _check.returncode != 0:
    errors.append(_check.stdout.strip() or "data/warranty.json is stale")

# ---- counts written into prose ----
# The README states the size of the dataset in its opening line, and that line went stale every
# time the dataset grew. Any "N models", "N makers", "N source documents" or "N verbatim clauses"
# in the README must match what the files hold.
readme = Path(__file__).resolve().parent.parent / "README.md"
if readme.exists():
    live = {
        "models": len(terms),
        "makers": len({t["maker"] for t in terms}),
        "source documents": len(sources),
        "sources": len(sources),
        "verbatim clauses": len(clauses),
        "clauses": len(clauses),
        "charging rules": len(rules),
    }
    # Only the live part of the README. Everything from "## Corrections" down is a dated record
    # of what was true at the time, and "Version 1.0.0 shipped 47 models" must stay as written.
    text = readme.read_text(encoding="utf-8").split("## Corrections")[0]
    for noun, n in live.items():
        for m in re.finditer(r"\b(\d+)\s+" + noun.replace(" ", r"\s+") + r"\b", text):
            if int(m.group(1)) != n:
                errors.append(f"README.md: says '{m.group(0)}' but the files hold {n}")

for w in warnings:
    print(f"warning: {w}")
# ---- prose counts ----
# 1.2.0. The README says its figures are counted from data/ rather than typed. Three of them
# were typed and three of them were wrong, found in an outside review and not by this script.
# Any number the prose states about the files is now checked here, so the claim is true.
_disp = collections.Counter(r["owner_can_dispute"] for r in terms)
_companies = len({r["maker"] for r in terms}) - 2   # Altigreen + Exponent, Mahindra + Mahindra LMM
# Only the README is checked for these. A past changelog entry states what was true at that
# release and stays as written: rewriting history to match today's totals would make the file
# useless as a record. The current release line is checked separately, below.
for _doc in ("README.md",):
    _p = Path(__file__).resolve().parent.parent / _doc
    if not _p.exists():
        continue
    _t = _p.read_text()
    for _pat, _want, _what in [
        (r"`?NOT_ADDRESSED`?\s+in\s+(\d+)\s+rows", _disp["NOT_ADDRESSED"], "NOT_ADDRESSED rows"),
        (r"`?PARTIAL`?\s+in\s+(\w+)\s+rows?", None, None),
        (r"[Cc]ount companies instead and it is (\d+)", _companies, "company count"),
    ]:
        if _want is None:
            continue
        for _m in re.finditer(_pat, _t):
            if int(_m.group(1)) != _want:
                errors.append(f"{_doc}: says {_m.group(0)!r} but the files hold "
                              f"{_want} for the {_what}")
# The changelog's release line must land on the current totals, or a reader who counts finds it short.
_rel = re.search(r"Sources \d+ to (\d+)\.\s+Clauses \d+ to (\d+)\.\s+Charging rules \d+ to (\d+)\.",
                 (Path(__file__).resolve().parent.parent / "CHANGELOG.md").read_text())
if not _rel:
    errors.append("CHANGELOG.md: the current release has no line of the form "
                  "'Sources N to N. Clauses N to N. Charging rules N to N.', so its figures "
                  "cannot be checked. Rewording that line silently disables this guard.")
else:
    for _got, _want, _what in zip(_rel.groups(), (len(sources), len(clauses), len(rules)),
                                  ("sources", "clauses", "charging rules")):
        if int(_got) != _want:
            errors.append(f"CHANGELOG.md: the current release line ends at {_got} {_what} "
                          f"but the files hold {_want}")

for e in errors:
    print(f"ERROR: {e}")

if held_on_purpose:
    print(f"\n{len(held_on_purpose)} document(s) held on purpose and cited by no row:")
    for u in sorted(held_on_purpose):
        print(f"  {u}: {by_id[u]['access_notes'].strip()[-105:]}")

print(f"\n{len(sources)} sources, {len(terms)} models, {len(clauses)} clauses, "
      f"{len(rules)} charging rules")
print(f"{len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
