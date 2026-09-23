# Contributing

## The one rule

Every value must come from a document published by the manufacturer: an official warranty page, an
owner's manual, or a warranty booklet. A blog, news article, aggregator, dealer site or comparison
site is never a source for a value. It may point you to the primary document, and then you cite the
document.

If you cannot find the value in a primary document, the correct contribution is a `NOT_FOUND` with a
note saying where you looked. An honest absence is worth more here than a filled cell, because the
absences are the finding.

## Adding or correcting a row

1. Add the document to `data/sources.csv` first, with a new `source_id`, the URL, the document type,
   the date you read it, and any access notes. If it was blocked to automated retrieval and you read
   it in a browser, say so.
2. Add or edit the row in `data/warranty-terms.csv`, referencing that `source_id`.
3. If the document contains a clause worth quoting, add it to `data/clauses.csv` **verbatim**. Do not
   paraphrase. The verbatim text is the product.
4. Set `model_scope` on any clause to the exact models whose documents you read it in. Not the maker,
   unless you read every one of that maker's documents and it is in all of them.
5. Run `python3 scripts/validate.py`. It must exit clean.
6. Add a line to `CHANGELOG.md`.

## Quoting

Keep quotes to the clause. This repository reports and compares warranty terms; it does not reproduce
manufacturers' documents. Quote the sentence that carries the obligation, not the page around it.

Typographic errors in the original stay in the quote. Several documents have them and they are part
of the record.

## Dates

ISO 8601, `YYYY-MM-DD`. The date is the date you personally opened the document, not the date the
document carries.

## What gets rejected

- A value with no source.
- A secondary source used as a primary one.
- A clause with no `model_scope`.
- A paraphrase in `clause_text`.
- A maker named as the subject of a clause found in only some of its documents.
- Removing a `NOT_FOUND` without adding the document that fills it.
