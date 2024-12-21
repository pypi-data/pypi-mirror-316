import httpj


def test_status_code_as_int():
    # mypy doesn't (yet) recognize that IntEnum members are ints, so ignore it here
    assert httpj.codes.NOT_FOUND == 404  # type: ignore[comparison-overlap]
    assert str(httpj.codes.NOT_FOUND) == "404"


def test_status_code_value_lookup():
    assert httpj.codes(404) == 404


def test_status_code_phrase_lookup():
    assert httpj.codes["NOT_FOUND"] == 404


def test_lowercase_status_code():
    assert httpj.codes.not_found == 404  # type: ignore


def test_reason_phrase_for_status_code():
    assert httpj.codes.get_reason_phrase(404) == "Not Found"


def test_reason_phrase_for_unknown_status_code():
    assert httpj.codes.get_reason_phrase(499) == ""
