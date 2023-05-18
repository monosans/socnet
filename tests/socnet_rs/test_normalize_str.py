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
    with pytest.raises(
        TypeError,
        match="argument 'text': 'int' object cannot be converted to 'PyString'",
    ):
        normalize_str(0)  # type: ignore[arg-type]
