from __future__ import annotations

from typing import TypeVar

import pytest

from socnet.core.utils import normalize_str

T = TypeVar("T")


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        ("string", "string"),
        (
            "\n\n \tstring\t  \n\n\n   string  \tstring  \n  \t ",
            "string\nstring string",
        ),
        (1, 1),
    ],
)
def test_normalize_str(given: T, expected: T) -> None:
    assert normalize_str(given) == expected
