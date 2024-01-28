#!/usr/bin/env python3
from __future__ import annotations

import sys


def main() -> None:
    from django.core.management import (  # noqa: PLC0415
        execute_from_command_line,
    )

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
