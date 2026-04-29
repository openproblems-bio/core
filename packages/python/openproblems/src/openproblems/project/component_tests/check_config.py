from __future__ import annotations

import re
from typing import Dict, List, Union

## CONSTANTS
NAME_MAXLEN = 50
LABEL_MAXLEN = 50
SUMMARY_MAXLEN = 400
DESCRIPTION_MAXLEN = 5000

TIME_LABELS = ["lowtime", "midtime", "hightime", "veryhightime"]
MEM_LABELS = ["lowmem", "midmem", "highmem", "veryhighmem"]
CPU_LABELS = ["lowcpu", "midcpu", "highcpu", "veryhighcpu"]


def check_url(url: str) -> bool:
    import requests
    from urllib3.util.retry import Retry
    from requests.adapters import HTTPAdapter

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    get = session.head(url)

    if get.ok or get.status_code == 429:  # 429 rejected, too many requests
        return True
    else:
        return False


def check_references(references: Dict[str, Union[str, List[str]]]) -> None:
    doi = references.get("doi")
    bibtex = references.get("bibtex")

    assert (
        doi or bibtex
    ), "One of .references.doi or .references.bibtex should be defined"

    if doi:
        if not isinstance(doi, list):
            doi = [doi]
        for d in doi:
            assert re.match(
                r"^10.\d{4,9}/[-._;()/:A-Za-z0-9]+$", d
            ), f"Invalid DOI format: {doi}"
            assert check_url(f"https://doi.org/{d}"), f"DOI '{d}' is not reachable"

    if bibtex:
        if not isinstance(bibtex, list):
            bibtex = [bibtex]
        for b in bibtex:
            assert re.match(r"^@.*{.*", b), f"Invalid bibtex format: {b}"


def check_links(
    links: Dict[str, Union[str, List[str]]], required: List[str] = []
) -> None:
    if not links:
        return

    for expected_link in required:
        assert expected_link in links, f"Link .links.{expected_link} is not defined"

    for link_type, link in links.items():
        if link_type != "docker_registry":
            assert check_url(
                link
            ), f"Link .links.{link_type} URL '{link}' is not reachable"


def check_info(this_info: Dict, this_config: Dict, comp_type: str) -> None:
    metadata_field_lengths = {
        "name": NAME_MAXLEN,
        "label": LABEL_MAXLEN,
        "summary": SUMMARY_MAXLEN,
        "description": DESCRIPTION_MAXLEN,
    }

    for field, max_length in metadata_field_lengths.items():
        value = this_info.get(field)
        if comp_type != "metric":
            value = this_config.get(field) or value
        assert value, f"Metadata field '{field}' is not defined"
        assert "FILL IN:" not in value, f"Metadata field '{field}' not filled in"
        assert (
            len(value) <= max_length
        ), f"Metadata field '{field}' should not exceed {max_length} characters"

    links = this_info.get("links") or this_config.get("links") or {}
    required_links: List[str] = []
    if comp_type == "method":
        required_links = ["documentation", "repository"]
    check_links(links, required_links)

    references = this_info.get("references") or {}
    if comp_type != "metric":
        references = this_config.get("references") or references
    if comp_type != "control_method" or references:
        print("Check references fields (doi or bibtex)", flush=True)
        check_references(references)


def check_config(config: dict) -> None:
    """Validate a viash component config.

    Checks namespace, info.type, component metadata, preferred_normalization,
    variants, and Nextflow runner labels.

    Args:
        config: Parsed viash config dict (from ``read_viash_config``).
    """
    info = config.get("info", {})
    comp_type = info.get("type")

    print("Check that .namespace is defined", flush=True)
    assert config.get("namespace"), ".namespace is not defined"

    print("Check that .info.type is 'method', 'control_method', or 'metric'", flush=True)
    expected_types = ["method", "control_method", "metric"]
    assert (
        comp_type in expected_types
    ), f".info.type is '{comp_type}' but should be one of: {', '.join(expected_types)}"

    print("Check component metadata fields (name, label, summary, description)", flush=True)
    if comp_type == "metric":
        metric_infos = info.get("metrics", [])
        assert metric_infos, ".info.metrics is not defined"
        for metric_info in metric_infos:
            check_info(metric_info, config, comp_type=comp_type)
    else:
        check_info(info, config, comp_type=comp_type)

    if "preferred_normalization" in info:
        print("Check that .info.preferred_normalization is a valid normalization method", flush=True)
        norm_methods = [
            "log_cpm",
            "log_cp10k",
            "counts",
            "log_scran_pooling",
            "sqrt_cpm",
            "sqrt_cp10k",
            "l1_sqrt",
        ]
        assert info["preferred_normalization"] in norm_methods, (
            ".info['preferred_normalization'] not one of '"
            + "', '".join(norm_methods)
            + "'."
        )

    if "variants" in info:
        print("Check that .info.variants only references valid argument names", flush=True)
        arg_names = [arg["clean_name"] for arg in config["all_arguments"]] + [
            "preferred_normalization"
        ]
        for paramset_id, paramset in info["variants"].items():
            if paramset:
                for arg_id in paramset:
                    assert arg_id in arg_names, (
                        f"Argument '{arg_id}' in `.info.variants['{paramset_id}']` "
                        "is not an argument in `.arguments`."
                    )

    runners = config.get("runners", [])

    print("Check that a Nextflow runner with time, mem, and cpu labels is defined", flush=True)
    nextflow_runner = next(
        (runner for runner in runners if runner["type"] == "nextflow"),
        None,
    )

    assert nextflow_runner, ".runners does not contain a nextflow runner"
    assert nextflow_runner.get(
        "directives"
    ), "directives not a field in nextflow runner"
    nextflow_labels = nextflow_runner["directives"].get("label")
    assert nextflow_labels, "label not a field in nextflow runner directives"

    assert [
        label for label in nextflow_labels if label in TIME_LABELS
    ], "time label not filled in"
    assert [
        label for label in nextflow_labels if label in MEM_LABELS
    ], "mem label not filled in"
    assert [
        label for label in nextflow_labels if label in CPU_LABELS
    ], "cpu label not filled in"

    print("All checks succeeded!", flush=True)
