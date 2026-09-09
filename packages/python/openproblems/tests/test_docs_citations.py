import copy
import os
import pytest

EXAMPLE_PROJECT = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        "data/example_project",
    )
)

TEMPLATE = "10.21203/rs.3.rs-4181617/v1"
ZAPPIA = "10.1371/journal.pcbi.1006245"
LUECKEN = "10.1038/s41592-021-01336-8"


def test_find_doi_citations_only_matches_pure_doi_brackets():
    from openproblems.project.docs._citations import find_doi_citations

    text = (
        f"tools exist [{ZAPPIA}] and benchmarks [{LUECKEN}; @{ZAPPIA}], "
        "but not bibtex keys [@luecken2022benchmarking], "
        f"mixed brackets [@key; {LUECKEN}], "
        f"or links [{ZAPPIA}](https://example.com)"
    )

    assert find_doi_citations(text) == [ZAPPIA, LUECKEN]


def test_rewrite_doi_citations_uses_pandoc_keys():
    from openproblems.project.docs._citations import rewrite_doi_citations

    text = f"one [{ZAPPIA}], then both [{LUECKEN}; {ZAPPIA}], not [@key]."

    assert rewrite_doi_citations(text) == (
        "one [@10.1371/journal.pcbi.1006245], then both "
        "[@10.1038/s41592-021-01336-8; @10.1371/journal.pcbi.1006245], not [@key]."
    )


def test_doi_key_is_a_valid_pandoc_citation_key():
    from openproblems.project.docs._citations import cite, doi_key

    # parentheses are legal in a DOI but not in a pandoc citation key
    assert doi_key("10.1016/S0092-8674(00)81683-9") == "10.1016/S0092-8674_00_81683-9"
    assert doi_key(ZAPPIA) == ZAPPIA
    assert cite([ZAPPIA, LUECKEN]) == f"[@{ZAPPIA}; @{LUECKEN}]"


def test_csl_reference_keeps_only_the_fields_citeproc_needs(fake_doi_org):
    from openproblems.project.docs._citations import csl_reference

    ref = csl_reference(ZAPPIA)

    assert fake_doi_org.calls == [ZAPPIA]
    assert ref["id"] == ZAPPIA
    assert "reference" not in ref
    assert ref["author"] == [
        {"family": "Zappia", "given": "Luke"},
        {"family": "Oshlack", "given": "Alicia"},
    ]
    assert ref["issued"] == {"date-parts": [[2018, 6, 25]]}
    # crossref's type vocabulary is mapped onto CSL's
    assert ref["type"] == "article-journal"


def test_csl_reference_fails_loudly_for_an_unresolvable_doi():
    from openproblems.project.docs._citations import csl_reference

    with pytest.raises(RuntimeError, match="Could not resolve DOI '10.1234/nope'"):
        csl_reference("10.1234/nope")


def test_render_task_readme_qmd_shows_license_and_task_doi_as_badges(fake_doi_org):
    from openproblems.project import render_task_readme_qmd

    result = render_task_readme_qmd(EXAMPLE_PROJECT)
    body = result.split("\n---\n", 1)[1]

    badges = (
        "[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) "
        "[![DOI](https://img.shields.io/badge/DOI-10.21203%2Frs.3.rs--4181617%2Fv1-blue.svg)]"
        "(https://doi.org/10.21203/rs.3.rs-4181617/v1)"
    )
    assert badges in body
    assert body.index(badges) < body.index("## Description")

    # a badge links to doi.org; only inline citations need a bibliography
    assert fake_doi_org.calls == []
    assert "references:" not in result
    assert "## References" not in result


def test_render_task_readme_qmd_resolves_inline_dois(fake_doi_org):
    from openproblems.project.docs import read_task_metadata
    from openproblems.project import render_task_readme_qmd

    task_metadata = copy.deepcopy(read_task_metadata(EXAMPLE_PROJECT))
    task_metadata["proj_conf"]["description"] = (
        f"Over 200 tools exist [{ZAPPIA}].\n"
        f"Several benchmarks exist [{LUECKEN}; {ZAPPIA}; {TEMPLATE}]."
    )

    result = render_task_readme_qmd(task_metadata)
    front_matter, body = result.split("\n---\n", 1)

    assert f"[@{ZAPPIA}]" in body
    assert f"[@{LUECKEN}; @{ZAPPIA}; @{TEMPLATE}]" in body
    # each DOI is resolved once, in order of first appearance
    assert fake_doi_org.calls == [ZAPPIA, LUECKEN, TEMPLATE]
    assert front_matter.startswith("---\ntitle: Template\nformat: gfm\nreferences:\n")
    assert f"- id: {ZAPPIA}" in front_matter
    assert "title: Benchmarking atlas-level data integration" in front_matter

    # citeproc appends the reference list under the closing header
    assert body.rstrip().endswith("## References")
    assert "{#refs}" not in body


def test_fetch_csl_resolves_a_doi_via_doi_org(fake_doi_org):
    from urllib.error import URLError

    try:
        csl = fake_doi_org.real("10.1093/nar/gkab004")
    except URLError as e:
        pytest.skip(f"doi.org not reachable: {e}")

    assert csl["DOI"].lower() == "10.1093/nar/gkab004"
    assert csl["author"][0]["family"] == "Chazarra-Gil"
    assert csl["issued"]["date-parts"][0][0] == 2021
