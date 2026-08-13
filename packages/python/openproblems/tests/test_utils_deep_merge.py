from openproblems.utils import deep_merge


def test_deep_merge_overrides_and_adds():
    out = deep_merge({"a": 1, "b": 2}, {"b": 3, "c": 4})
    assert out == {"a": 1, "b": 3, "c": 4}


def test_deep_merge_is_recursive():
    out = deep_merge({"a": {"b": 1, "c": 2}}, {"a": {"c": 3}})
    assert out == {"a": {"b": 1, "c": 3}}


def test_deep_merge_appends_lists():
    assert deep_merge([1, 2], [3]) == [1, 2, 3]


def test_deep_merge_preserves_key_order():
    out = deep_merge({"b": 1, "a": 2}, {"d": 3, "c": 4, "a": 5})
    assert list(out.keys()) == ["b", "a", "d", "c"]
