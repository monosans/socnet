from __future__ import annotations

import pytest

from socnet_rs import minify_html


@pytest.mark.parametrize(
    ("given", "expected"),
    [("<html></html>", ""), ('<input type="text" />', "<input>")],
)
def test_minify_html(given: str, expected: str) -> None:
    assert minify_html(given) == expected


def test_type_error() -> None:
    exc_str = "argument 'value': 'int' object cannot be converted to 'PyString'"
    with pytest.raises(TypeError, match=exc_str):
        minify_html(0)  # type: ignore[arg-type]
