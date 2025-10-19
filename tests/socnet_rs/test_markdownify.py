from __future__ import annotations

import pytest

from socnet_rs import markdownify


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        ("# Header", "<h1>Header</h1>\n"),
        (
            '<p>Paragraph</p><script>alert("Dangerous code")</script>',
            "<p>Paragraph</p>",
        ),
    ],
)
def test_markdownify(given: str, expected: str) -> None:
    assert markdownify(given) == expected


def test_type_error() -> None:
    exc_str = "argument 'value': 'int' object cannot be cast as 'str'"
    with pytest.raises(TypeError, match=exc_str):
        markdownify(0)  # type: ignore[arg-type]
