#!/usr/bin/env python3
from __future__ import annotations

if __name__ == "__main__":
    import logging
    import os
    from argparse import ArgumentParser

    import granian.constants
    import granian.log
    from granian import Granian

    from config.settings.logging import LOGGING

    parser = ArgumentParser()
    parser.add_argument("--prod", action="store_true")
    args = parser.parse_args()

    for log_level in granian.log.LogLevels:
        granian.log.log_levels_map[log_level] = logging.NOTSET
    Granian(
        target="config.asgi:application",
        address="0.0.0.0",  # noqa: S104
        port=8000,
        interface=granian.constants.Interfaces.ASGINL,
        workers=(os.cpu_count() or 1) if args.prod else 1,
        log_dictconfig=LOGGING,
        log_access=True,
        reload=not args.prod,
    ).serve()
