#!/usr/bin/env python3
from __future__ import annotations

if __name__ == "__main__":
    import logging.config

    from config.settings.logging import LOGGING

    logging.config.dictConfig(LOGGING)

    from django.core.management import execute_from_command_line

    execute_from_command_line()
