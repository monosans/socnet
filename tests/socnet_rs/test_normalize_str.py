from __future__ import annotations

import pytest

from socnet_rs import normalize_str


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        ("string", "string"),
        (
            "\n\n \tstring\t  \n\n\n   string  \tstring  \n  \t ",
            "string\nstring string",
        ),
    ],
)
def test_normalize_str(given: str, expected: str) -> None:
    assert normalize_str(given) == expected


def test_type_error() -> None:
    exc_str = "argument 'value': 'int' object cannot be cast as 'str'"
    with pytest.raises(TypeError, match=exc_str):
        normalize_str(0)  # type: ignore[arg-type]
