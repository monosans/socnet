#!/usr/bin/env python3
from __future__ import annotations

if __name__ == "__main__":
    import logging.config

    from config.settings.log import LOG_CONFIG

    logging.config.dictConfig(LOG_CONFIG)

    from django.core.management import execute_from_command_line

    execute_from_command_line()
