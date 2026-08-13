from typing import Any, Dict

import pytest

from openproblems.project import check_config


def _config(**kwargs: Any) -> Dict[str, Any]:
    # a control method without links or references, so that check_config
    # does not need network access to validate the metadata
    config: Dict[str, Any] = {
        "name": "foo",
        "label": "Foo",
        "summary": "A foo control method.",
        "description": "A foo control method.",
        "namespace": "control_methods",
        "info": {"type": "control_method"},
        "runners": [
            {
                "type": "nextflow",
                "directives": {"label": ["lowtime", "lowmem", "lowcpu"]},
            }
        ],
    }
    config.update(kwargs)
    return config


def test_check_config_accepts_resource_labels():
    check_config(_config())


def test_check_url_passes_a_timeout_and_survives_a_failure():
    import requests
    from unittest import mock
    from openproblems.project.component_tests.check_config import (
        URL_TIMEOUT,
        check_url,
    )

    with mock.patch.object(requests.Session, "head") as head:
        head.return_value = mock.Mock(ok=True, status_code=200)
        assert check_url("https://example.com")
        assert head.call_args.kwargs["timeout"] == URL_TIMEOUT

        head.side_effect = requests.exceptions.ConnectTimeout()
        assert not check_url("https://example.com")


def test_check_links_requires_the_expected_links():
    from openproblems.project.component_tests.check_config import check_links

    for links in [{}, None, {"documentation": "https://example.com"}]:
        with pytest.raises(AssertionError, match="Link .links.repository"):
            check_links(links, ["repository"])


def test_check_config_requires_a_nextflow_runner():
    with pytest.raises(AssertionError, match="does not contain a nextflow runner"):
        check_config(_config(runners=[{"type": "executable"}]))


def test_check_config_requires_resource_labels():
    with pytest.raises(AssertionError, match="directives not a field"):
        check_config(_config(runners=[{"type": "nextflow"}]))

    runners = [{"type": "nextflow", "directives": {"tag": "$id"}}]
    with pytest.raises(AssertionError, match="label not a field"):
        check_config(_config(runners=runners))


def test_check_config_requires_a_label_of_each_kind():
    for labels, message in [
        (["lowmem", "lowcpu"], "time label not filled in"),
        (["lowtime", "lowcpu"], "mem label not filled in"),
        (["lowtime", "lowmem"], "cpu label not filled in"),
    ]:
        runners = [{"type": "nextflow", "directives": {"label": labels}}]
        with pytest.raises(AssertionError, match=message):
            check_config(_config(runners=runners))


def test_check_config_skips_resource_labels_for_nextflow_workflows():
    # viash renders a nextflow_script component as a workflow rather than a
    # process, so it has nothing to attach resource labels to
    resources = [{"type": "nextflow_script", "path": "main.nf", "entrypoint": "run_wf"}]
    check_config(
        _config(
            resources=resources,
            runners=[{"type": "nextflow"}],
        )
    )
