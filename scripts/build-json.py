#!/usr/bin/env python3
"""Generate data/warranty.json from the CSVs.

The JSON used to be maintained by hand and it drifted. At 1.1.3 it carried 54 sources, 67 models
and 63 clauses in its arrays, a `counts` field claiming 56, 67 and 71, and the CSVs beside it
held 56, 67 and 71. A published artifact that disagrees with itself and with its own source of
truth is the one defect this dataset exists to avoid, so it is generated now and the validator
regenerates and compares on every run.

    python3 scripts/build-json.py            # write it
    python3 scripts/build-json.py --check    # exit 1 if the file on disk is stale
"""
import csv, json, sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data"
OUT = D / "warranty.json"

VERSION = "1.2.0"
PUBLISHED = "2026-10-04"

ABSENCE_CODES = {
    "NOT_FOUND": "Looked for and not located in any document read.",
    "NOT_STATED": "The document was read and does not address this.",
    "NOT_DISCLOSED": "The document says the thing exists and does not say what it is.",
    "NOT_ADDRESSED": "The document is silent on whether the owner has any route to dispute.",
    "NO_FIGURE_IN_DOCUMENT": "The document discusses this and prints no number.",
    "PARTIAL": "Some of it is stated and some is not. The notes say which.",
    "DISCLOSED": "Stated in full.",
    "EXCLUDED": "The document addresses this and puts it outside cover. Stronger than NOT_STATED.",
}


def rows(name):
    with open(D / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build():
    sources = rows("sources.csv")
    models = rows("warranty-terms.csv")
    clauses = rows("clauses.csv")
    charging = rows("charging-rules.csv")
    return {
        "dataset": "india-ev-battery-warranty",
        "version": VERSION,
        "published": PUBLISHED,
        "licence": "CC BY 4.0",
        "maintainer": "Voltu",
        # Generated from the arrays below, so these can never disagree with them again.
        "counts": {
            "sources": len(sources),
            "makers": len({m["maker"] for m in models}),
            "models": len(models),
            "clauses": len(clauses),
            "charging_rules": len(charging),
        },
        "absence_codes": ABSENCE_CODES,
        "sources": sources,
        "models": models,
        "clauses": clauses,
        "charging_rules": charging,
    }


def serialise(obj):
    return json.dumps(obj, indent=1, ensure_ascii=False) + "\n"


if __name__ == "__main__":
    want = serialise(build())
    if "--check" in sys.argv:
        have = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if have != want:
            print("data/warranty.json is stale. Run python3 scripts/build-json.py")
            sys.exit(1)
        print("data/warranty.json is current")
    else:
        OUT.write_text(want, encoding="utf-8")
        c = build()["counts"]
        print(f"data/warranty.json written: {c['sources']} sources, {c['makers']} makers, "
              f"{c['models']} models, {c['clauses']} clauses, {c['charging_rules']} charging rules")
