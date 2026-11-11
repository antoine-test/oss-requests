from requests.profiles import build_session, merge_profiles


def test_build_session_sets_headers():
    session = build_session({"headers": {"X-Test": "1"}})
    assert session.headers["x-test"] == "1"


def test_build_session_mounts_adapter():
    session = build_session({"headers": {}})
    assert "https://" in session.adapters


def test_merge_profiles_prefers_override():
    merged = merge_profiles(
        {"headers": {"A": "1", "B": "1"}}, {"headers": {"B": "2"}}
    )
    assert merged["headers"] == {"A": "1", "B": "2"}
