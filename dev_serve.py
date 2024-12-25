#!/usr/bin/env python3
from __future__ import annotations

if __name__ == "__main__":
    import uvicorn

    from config.settings.log import LOG_CONFIG

    uvicorn.run(
        "config.asgi:application",
        host="0.0.0.0",  # noqa: S104
        port=8000,
        reload=True,
        reload_includes=["*.html"],
        log_config=LOG_CONFIG,
        server_header=False,
        use_colors=False,
    )
