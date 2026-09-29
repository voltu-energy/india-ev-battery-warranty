# India EV Battery Warranty Dataset

Every electric vehicle battery warranty sold in India, read at the manufacturer's own document.
67 models, 31 makers, 54 source documents, 63 verbatim clauses, four wheel and two and three wheel.
Every figure here is counted from `data/` rather than typed, because the last three times one was
typed it was wrong.

The maker figure counts distinct values in the `maker` column, so a pack warranted by a third party
counts separately from the vehicle maker: Altigreen and Altigreen / Exponent are two, as are Mahindra
and Mahindra Last Mile Mobility. Count companies instead and it is 29.

Version 1.1.0, published 28 September 2026. Documents read 22 September 2026, with the makers added
in 1.1.0 read 28 September 2026.

## Why this exists

If you buy an electric vehicle in India, the most expensive component in it is warranted against a
number you cannot see, measured by a method no document describes, assessed by the party that pays
if the answer goes your way.

That sentence is easy to assert and hard to prove, so this repository is the proof. Every cell
traces to a manufacturer document, with the URL and the date it was read.

Four things this dataset establishes, and each one is checkable from the files:

- **Of 67 models, two name a condition under which state of health is measured and none sets out a
  procedure.** The Altigreen neEV TEZ, whose pack is warranted by Exponent, specifies a CC-CV profile
  at 54A. Hero Electric states replacement thresholds in amp-hours for a 30Ah battery at C5 discharge
  rate. Neither gives a temperature, a state of charge window, a rest period or an instrument, so
  neither is a procedure an owner or a third party could follow and repeat. Every other maker that
  publishes a threshold leaves the measurement wholly undefined.
- **One maker excludes battery degradation from its battery warranty in terms.** BYD India warrants
  the traction battery for 8 years / 160,000 km and then excludes "the normal attenuation of battery
  capacity" from the scope of that warranty, while stating no state of health floor anywhere in the
  document. The headline term covers failure, not the loss of range the buyer is worried about.
- **No model grants the owner an independent right to verify or dispute the reading.** This is the
  finding that holds at 67 out of 67. The `owner_can_dispute` column is an absence code in every row
  but two, and both of those say so in their own terms: Mercedes-Benz makes the baseline obtainable
  but offers no dispute route, and Exponent requires a report within seven days while granting no
  independent right.
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
| `data/sources.csv` | One row per document. URL, type, date read, how it was reached, and what it was: `sha256` of the PDF we read, and `archive_url` for a dated capture. |
| `data/warranty.json` | All three, joined, for anyone who would rather not parse CSV. |
| `scripts/validate.py` | Enforces the sourcing rule. Run it before any pull request. |


## When a source stops serving

Every value here is read at a manufacturer's or a government's own document. That only stays checkable
while the document stays up, and on 29 September 2026 it did not: four of five BYD India asset URLs
that search engines had indexed stopped serving inside about a week, including all three warranty
policies. Those rows survived because the files had been saved by hand.

So each source row records what the document was, not only where it was:

- **`sha256`** for a PDF. It does not bring the file back. It lets anyone who obtains a copy by any
  route prove it is the document we read.
- **`archive_url`** for a dated capture, which is the right artefact for a web page. Hashing HTML is
  noise, because the page changes on every render. For two of the BYD documents the Internet Archive
  capture of BYD's own asset host is now the only first-party copy that serves.

`scripts/freeze-sources.py` fills both in, and on a re-run verifies rather than overwrites. A hash
that no longer matches is not an error to write over. It means a maker has edited a document under
us, which is a finding, and the script reports it and exits non-zero.

    python3 scripts/freeze-sources.py            # fill in what is missing
    python3 scripts/freeze-sources.py --check    # verify only, for CI

It needs ordinary outbound internet and will not run behind an egress allowlist.

## Absence codes, and why there are seven of them

A blank cell would hide the most interesting thing in the dataset, so there are no blank cells.

| Code | Meaning |
|---|---|
| `NOT_FOUND` | No primary document stating this was located. Where we looked is in the notes. |
| `NOT_STATED` | The document was read and does not state this. |
| `NOT_DISCLOSED` | The document sets a threshold but does not describe how it is measured. |
| `NOT_ADDRESSED` | The document does not contemplate this at all. |
| `NO_FIGURE_IN_DOCUMENT` | The full text was searched and contains no percentage of any kind. Used for MG. |
| `PARTIAL` | Addressed in part only. See the notes on that row. |
| `EXCLUDED` | The document addresses this and puts it outside cover. Not a gap; the opposite of one. |

`warranty.json` carries these under `absence_codes` together with `DISCLOSED`, which is not an
absence but a present-value code for a row where a measurement method is described.

`NOT_FOUND` and `NOT_STATED` are different claims and the difference matters. The first says we could
not find the document. The second says we read it and it is silent.

## Scope, which is a rule and not a disclaimer

**A clause belongs to the documents it appears in, not to the maker.**

Tata is the reason this rule exists. Its seven EV owner manuals are not uniform: the DC charging cap
is in five of them, the telematics requirement in six, the charging warning limit in three. So
`clauses.csv` carries a `model_scope` column and the validator rejects a clause without one.

"Five of Tata's seven EV owner manuals cap DC fast charging" is supported by this dataset.
"Tata caps DC fast charging" is not.

The same applies to the dataset as a whole. It covers 67 models. "No model in this dataset" is a
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

**1.1.0, 28 September 2026. Six makers were missing, and the published counts were wrong.**

Version 1.0.0 shipped 47 models and claimed 25 makers. The maker figure was in no file at any point;
the maker column held 24 distinct values. Counting it properly exposed the real defect: six makers the
audit had read never reached `warranty-terms.csv` at all.

**Ultraviolette, PMV Electric, Audi India, Euler Motors, Strom Motors, Hero Electric.** Seven rows,
one per model, each read at the maker's own site on 28 September 2026:

- **Ultraviolette** was not an absence at all. The Tesseract carries 8 years and 200,000 km and the
  F77 up to 1,00,000 km, stated on the model pages because the company publishes no warranty booklet.
- **PMV Electric** states no warranty term anywhere. Its FAQ offers an expectation instead: cells
  "anticipated" to last 5-8 years, based on the cell manufacturer's warranty rather than PMV's.
- **Audi India** publishes a warranty page with no high voltage battery term of any kind, repair or
  replacement at its "sole discretion", and refers the reader to a booklet it does not publish.
- **Euler Motors** carries no warranty term on the HiLoad product page, and its terms and conditions
  URL returns AccessDenied.
- **Strom Motors** and **Hero Electric** serve no warranty document at all. Both were confirmed by a
  browser pass on 28 September 2026 after automated retrieval failed, and both are recorded with
  `document_type = none_located` and the URL that was reached.

Two absence-aware source types were added to make those records expressible rather than droppable:
`official_faq_page` and `none_located`. A maker that publishes nothing is a finding, and a finding
needs a row. The previous release silently omitted them, which is the one failure this dataset cannot
afford.

**Also added in 1.1.0, after a model-level check against the audit.** Tesla India, absent entirely:
Model Y Premium RWD at 8 years / 160,000 km and Model Y L at 8 years / 192,000 km, both with a stated
70% retention floor, no method and no dispute route. And five Mercedes-Benz models whose terms differ
from the EQA/EQB/EQC/EQG row that stood alone in 1.0.0: EQS 580 4MATIC at 8 years / unlimited, EQS
580 SUV at 10 years / unlimited, and EQS 53 AMG, EQE 500 4M SUV and Maybach EQS 680 at 10 years /
250,000 km. The dataset had been keeping each maker's base tier and losing the rest, which understated
the spread of terms in the market and lost the longest warranty in it.

**Hero Electric, added 29 September 2026 from the maker's own booklet**, and it is the most
conditional warranty in the dataset. Three years, private use only. Commercial use drops it to one
year on the bike and two on the battery, and private use is defined as consuming **up to 75% of
charge per day** — take more than that and you are reclassified as commercial. The replacement
threshold is not a percentage but a figure in amp-hours that steps down with age: below 22Ah in the
first six months, below 18Ah to month 24, below 16Ah to month 36, stated for a 30Ah battery **at C5
discharge rate**.

That C5 reference matters to the headline above and is flagged, not settled. It names a test
condition, which is more than any other maker except Exponent offers, but it stops short of a
procedure. It is coded `PARTIAL` pending a reading of the Hindi original by someone who reads Hindi.

**BYD India: all four models read on 29 September 2026, and they are not the same document.** The
ATTO 3 and Seal policies carry a full Warranty Limitations and Exclusions section. The eMAX 7 and
Sealion 7 documents carry the warranty period table and no exclusions section at all: they refer the
reader to "the further policies from BYD in its official website", which they do not contain. So the
attenuation exclusion is recorded for the ATTO 3 and Seal only, and the eMAX 7 and Sealion 7 rows are
`NOT_STATED`, not `EXCLUDED`. All four publish the same 8 year / 160,000 km traction battery term.

 The ATTO 3 Booking and Warranty Policy was obtained
and read in full. It sets the traction battery at 8 years / 160,000 km, excludes normal capacity
attenuation at clause 8, allows replacement with a reconditioned or re-manufactured part at BYD's sole
discretion while conceding the result "may not restore the vehicle to a 'like new' condition", gives a
replaced part only the remainder of the original part's term, and lists failure to install a notified
software update among the things that may void warranty service. Five clauses recorded verbatim. The
document was searched in full for any capacity retention figure: there is none.

**Known gaps, stated rather than hidden.** The BYD documents are held as files rather than at a
citable BYD URL, because `bydautoindia.com` does not serve to European networks; the source rows carry
the canonical host and note that a per-document URL is to be substituted once it is reachable. **Strom Motors is closed, and closed the right way.** Its site was unreachable from a European
network on 28 September, which is not evidence of anything. Retrieved successfully from a third
network on 29 September: the site is live, serves marketing content and a pre-booking call to action,
and links no warranty page, no owner's manual and no terms document. The absence now rests on a
successful read of a live site rather than on a failed one, which is the only way an absence should
ever be recorded here.

**Tata XPRES-T EV, the largest known gap at 1.0.0, is closed.** Its warranty chapter begins on page
145 and has now been read. The fleet and taxi variant is warranted "Inclusive of Battery and Electric
Powertrain" for **3 years or 1,25,000 km** — the shortest battery term of any Tata EV here, against
lifetime terms on the passenger models. The highest-utilisation vehicle carries the least cover.

Nothing in the original 47 rows changed except the Hero MotoCorp note, which now records the paid
Advantage extension to 5 years / 60,000 km. `clauses.csv` is unchanged: no new clause text was found
to quote.

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
