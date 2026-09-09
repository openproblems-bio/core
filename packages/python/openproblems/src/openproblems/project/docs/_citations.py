"""DOI citations in task READMEs.

A description may cite literature by DOI, using pandoc's citation syntax with
the DOI in place of a bibtex key: ``[10.1038/s41592-021-01336-8]`` or
``[10.1038/s41592-021-01336-8; 10.1186/s13059-019-1850-9]``. Each DOI is
resolved to CSL-JSON through doi.org content negotiation (the same source the
website uses) and put in the document's ``references`` metadata, and the
bracket is rewritten to a pandoc citation keyed by the DOI, so quarto's
citeproc renders the citation and the reference list.

Brackets that hold bibtex keys (``[@key]``) or a mix of both are left alone.
"""
from __future__ import annotations

import json
import re
import urllib.request

# the DOI format check_config accepts, optionally with pandoc's leading `@`
_DOI_TOKEN = re.compile(r"^@?(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)$")

# `[...]` that is not a markdown link or reference (`[text](url)`, `[text][ref]`)
_BRACKET = re.compile(r"\[([^\[\]]+)\](?![\[(])")

# pandoc citation keys allow alphanumerics, `_` and these punctuation characters
_KEY_UNSAFE = re.compile(r"[^A-Za-z0-9_:.#$%&+?<>~/-]")

# the CSL-JSON fields citeproc needs; doi.org also returns the full reference
# list, funders, licenses, ... which would bloat the front matter
_CSL_FIELDS = (
    "type",
    "title",
    "author",
    "issued",
    "container-title",
    "volume",
    "issue",
    "page",
    "publisher",
    "DOI",
    "URL",
)
_AUTHOR_FIELDS = ("family", "given", "literal")

# crossref uses its own type vocabulary; citeproc only knows the CSL one and
# falls back to a generic entry for anything else
_CSL_TYPES = {
    "journal-article": "article-journal",
    "proceedings-article": "paper-conference",
    "book-chapter": "chapter",
    "posted-content": "article",
    "dissertation": "thesis",
    "peer-review": "review",
}


def _bracket_dois(bracket: str) -> list[str] | None:
    """The DOIs in one bracket, or None when any token is not a DOI."""
    dois = []
    for token in bracket.split(";"):
        match = _DOI_TOKEN.match(token.strip())
        if not match:
            return None
        dois.append(match.group(1))
    return dois


def find_doi_citations(text: str) -> list[str]:
    """Unique DOIs cited inline in ``text``, in order of first appearance."""
    found: list[str] = []
    for bracket in _BRACKET.finditer(text):
        for doi in _bracket_dois(bracket.group(1)) or []:
            if doi not in found:
                found.append(doi)
    return found


def doi_key(doi: str) -> str:
    """Turn a DOI into a valid pandoc citation key."""
    return _KEY_UNSAFE.sub("_", doi)


def cite(dois: list[str]) -> str:
    """A pandoc citation of these DOIs, e.g. ``[@10.1/a; @10.2/b]``."""
    return "[" + "; ".join(f"@{doi_key(doi)}" for doi in dois) + "]"


def rewrite_doi_citations(text: str) -> str:
    """Rewrite inline DOI citations in ``text`` to pandoc citations."""

    def rewrite(match: re.Match) -> str:
        dois = _bracket_dois(match.group(1))
        return match.group(0) if dois is None else cite(dois)

    return _BRACKET.sub(rewrite, text)


def fetch_csl(doi: str) -> dict:
    """Fetch the CSL-JSON record for a DOI from doi.org."""
    request = urllib.request.Request(
        f"https://doi.org/{doi}",
        headers={"Accept": "application/vnd.citationstyles.csl+json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def csl_reference(doi: str) -> dict:
    """Resolve a DOI to a CSL reference for the document's ``references``."""
    try:
        csl = fetch_csl(doi)
    except Exception as e:
        raise RuntimeError(f"Could not resolve DOI '{doi}' via doi.org") from e

    reference: dict = {"id": doi_key(doi)}
    for field in _CSL_FIELDS:
        if field in csl:
            reference[field] = csl[field]
    if "type" in csl:
        reference["type"] = _CSL_TYPES.get(csl["type"], csl["type"])
    if "author" in csl:
        reference["author"] = [
            {k: author[k] for k in _AUTHOR_FIELDS if k in author}
            for author in csl["author"]
        ]
    return reference
