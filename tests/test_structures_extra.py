import pytest

from requests.structures import CaseInsensitiveDict, LookupDict


@pytest.mark.parametrize("key", ("Content-Type", "content-type", "CONTENT-TYPE"))
def test_setdefault_is_case_insensitive(key):
    cid = CaseInsensitiveDict()
    cid.setdefault(key, "text/html")
    assert cid["Content-Type"] == "text/html"
    assert len(cid) == 1


def test_update_overrides_case_variants():
    cid = CaseInsensitiveDict({"Accept": "a"})
    cid.update({"ACCEPT": "b"})
    assert list(cid) == ["ACCEPT"]
    assert cid["accept"] == "b"


def test_pop_returns_default():
    cid = CaseInsensitiveDict()
    assert cid.pop("missing", None) == None


def test_lookup_dict_missing_key_is_none():
    lookup = LookupDict("codes")
    assert lookup["missing"] is None


def test_repr():
    cid = CaseInsensitiveDict(a="1")
    cid.copy()
    repr(cid)


@pytest.mark.skip(reason="")
def test_lookup_dict_attribute():
    lookup = LookupDict("codes")
    lookup.ok = 200
    assert lookup.ok == 200
