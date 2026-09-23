# India EV Battery Warranty Dataset

Every electric vehicle battery warranty sold in India, read at the manufacturer's own document.
47 models, 25 makers, 41 source documents, four wheel and two and three wheel.

Version 1.0.0, published 23 September 2026. Documents read 22 September 2026.

## Why this exists

If you buy an electric vehicle in India, the most expensive component in it is warranted against a
number you cannot see, measured by a method no document describes, assessed by the party that pays
if the answer goes your way.

That sentence is easy to assert and hard to prove, so this repository is the proof. Every cell
traces to a manufacturer document, with the URL and the date it was read.

Four things this dataset establishes, and each one is checkable from the files:

- **Of 47 models, one discloses how state of health is measured.** The Altigreen neEV TEZ, whose
  pack is warranted by Exponent, which specifies a CC-CV profile at 54A. Every other maker that
  publishes a threshold leaves undefined the procedure that produces the number the threshold is
  compared against.
- **No model grants the owner a right to verify or dispute the reading.** The `owner_can_dispute`
  column is an absence code in every row but two, and both of those are partial.
- **Some warranties impose charging conditions most owners never see.** Five of Tata's seven EV owner
  manuals make it a condition that after four DC charges you charge to 100 percent on AC. Six of the
  seven require a live telematics subscription, because that is how the maker sees the pack. None of
  it appears on the warranty web page a buyer is directed to.
- **The absences are half the finding.** A cell reading NOT_FOUND is a result, not a gap in the work.

## The files

| File | What it is |
|---|---|
| `data/warranty-terms.csv` | One row per model. Term in years and km, state of health floor, who measures, whether a method is disclosed, whether the owner can dispute. |
| `data/clauses.csv` | One row per clause, quoted verbatim, with the models it applies to. |
| `data/sources.csv` | One row per document. URL, type, date read, and how it was reached. |
| `data/warranty.json` | All three, joined, for anyone who would rather not parse CSV. |
| `scripts/validate.py` | Enforces the sourcing rule. Run it before any pull request. |

## Absence codes, and why there are six of them

A blank cell would hide the most interesting thing in the dataset, so there are no blank cells.

| Code | Meaning |
|---|---|
| `NOT_FOUND` | No primary document stating this was located. Where we looked is in the notes. |
| `NOT_STATED` | The document was read and does not state this. |
| `NOT_DISCLOSED` | The document sets a threshold but does not describe how it is measured. |
| `NOT_ADDRESSED` | The document does not contemplate this at all. |
| `NO_FIGURE_IN_DOCUMENT` | The full text was searched and contains no percentage of any kind. Used for MG. |
| `PARTIAL` | Addressed in part only. See the notes on that row. |

`NOT_FOUND` and `NOT_STATED` are different claims and the difference matters. The first says we could
not find the document. The second says we read it and it is silent.

## Scope, which is a rule and not a disclaimer

**A clause belongs to the documents it appears in, not to the maker.**

Tata is the reason this rule exists. Its seven EV owner manuals are not uniform: the DC charging cap
is in five of them, the telematics requirement in six, the charging warning limit in three. So
`clauses.csv` carries a `model_scope` column and the validator rejects a clause without one.

"Five of Tata's seven EV owner manuals cap DC fast charging" is supported by this dataset.
"Tata caps DC fast charging" is not.

The same applies to the dataset as a whole. It covers 47 models. "No model in this dataset" is a
claim you can make from it. "No maker in India" is not.

## What this dataset is not

It is not a measurement. Nothing here was tested, sampled or modelled. It is a reading of published
documents and nothing more.

It is not an accusation. A warranty needs a threshold, a threshold needs a measurement, and no Indian
standard defines how state of health is measured in service. AIS-038, AIS-156, AIS-040 and AIS-049
are type approval instruments that test a new vehicle. The Ministry of Road Transport and Highways
says as much in its own draft Battery Pack Aadhaar guidelines: "The detailed methodology for
validating SOH needs to be separately developed by the Government." Every maker here is operating
inside that vacuum.

It is not complete. See `CHANGELOG.md` for the known gaps at first publication.

## Corrections

Open an issue with the document attached, or a pull request. If you work for one of the manufacturers
listed and we have a cell wrong, that is the most useful issue this repository can receive, and it
will be corrected in public with the date and with credit to whoever caught it.

One condition: send the primary document. Not coverage of it, not a dealer page, not a comparison
site. That rule is what the dataset is for.

If you would rather not open a GitHub account, write to hello@voltu.energy with the document attached
and we will file the issue ourselves, crediting you.

## Licence

Data under `data/` is CC BY 4.0. Scripts are MIT. See `LICENSE`.

## Who maintains this

Voltu, which is building an independent measurement of EV charging reliability in India. The first
Mumbai index publishes on 5 November 2026.

We publish this because the same gap runs through both subjects. A charging network reports its own
uptime. A manufacturer measures its own battery. In each case the number that matters most is
produced by the party with the most at stake in the answer, and in each case the reason is not malice,
it is that nobody else is counting.

voltu.energy
