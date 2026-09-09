import copy
from types import SimpleNamespace

import pytest

# what doi.org returns for a DOI, trimmed to the fields that matter here
FAKE_CSL = {
    # the example project's own reference
    "10.21203/rs.3.rs-4181617/v1": {
        "type": "posted-content",
        "title": "A template for creating new tasks",
        "author": [{"family": "Doe", "given": "John"}],
        "issued": {"date-parts": [[2021]]},
        "publisher": "Research Square",
        "DOI": "10.21203/rs.3.rs-4181617/v1",
    },
    "10.1371/journal.pcbi.1006245": {
        "type": "journal-article",
        "title": "Exploring the single-cell RNA-seq analysis landscape",
        "author": [
            {"family": "Zappia", "given": "Luke", "affiliation": []},
            {"family": "Oshlack", "given": "Alicia", "affiliation": []},
        ],
        "issued": {"date-parts": [[2018, 6, 25]]},
        "container-title": "PLOS Computational Biology",
        "DOI": "10.1371/journal.pcbi.1006245",
        "reference": [{"key": "not wanted in the readme"}],
    },
    "10.1038/s41592-021-01336-8": {
        "type": "journal-article",
        "title": "Benchmarking atlas-level data integration",
        "author": [{"family": "Luecken", "given": "Malte D."}],
        "issued": {"date-parts": [[2021, 12, 23]]},
        "container-title": "Nature Methods",
        "DOI": "10.1038/s41592-021-01336-8",
    },
}


@pytest.fixture(autouse=True)
def fake_doi_org(monkeypatch):
    """Serve DOI lookups from FAKE_CSL so the tests stay offline.

    ``calls`` records the DOIs looked up; ``real`` is the actual doi.org lookup.
    """
    from openproblems.project.docs import _citations

    fake = SimpleNamespace(calls=[], real=_citations.fetch_csl)

    def fetch(doi):
        fake.calls.append(doi)
        return copy.deepcopy(FAKE_CSL[doi])

    monkeypatch.setattr(_citations, "fetch_csl", fetch)
    return fake
