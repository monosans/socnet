#!/usr/bin/env python3
from __future__ import annotations

if __name__ == "__main__":
    import os
    from argparse import ArgumentParser

    import granian.constants
    import granian.log
    from granian import Granian

    from config.settings.log import LOG_CONFIG

    parser = ArgumentParser()
    parser.add_argument("--prod", action="store_true")
    args = parser.parse_args()

    Granian(
        target="config.asgi:application",
        address="0.0.0.0",  # noqa: S104
        port=8000,
        interface=granian.constants.Interfaces.ASGINL,
        workers=(os.cpu_count() or 1) if args.prod else 1,
        http=granian.constants.HTTPModes.http1,
        log_level=granian.log.LogLevels.notset,
        log_dictconfig=LOG_CONFIG,
        log_access=True,
        reload=not args.prod,
    ).serve()
