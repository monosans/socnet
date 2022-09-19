from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def normalize_str(value: T) -> T:
    if not isinstance(value, str):
        return value
    return "\n".join(  # type: ignore[return-value]
        " ".join(line.split())
        for line in filter(None, (line.strip() for line in value.splitlines()))
    )
