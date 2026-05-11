#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wait until MySQL accepts connections (used by Docker entrypoint)."""

from __future__ import annotations

import os
import sys
import time

import pymysql
from sqlalchemy.engine.url import make_url


def main() -> int:
    raw = os.environ.get("DATABASE_URL", "")
    if "mysql" not in raw:
        return 0

    url = make_url(raw)
    if (url.drivername or "") != "mysql+pymysql":
        print("wait_for_mysql: expected mysql+pymysql URL", file=sys.stderr)
        return 1

    deadline = time.time() + 90
    last_err: Exception | None = None
    while time.time() < deadline:
        try:
            conn = pymysql.connect(
                host=url.host or "127.0.0.1",
                port=url.port or 3306,
                user=url.username or "root",
                password=url.password or "",
                database=url.database,
                connect_timeout=3,
            )
            conn.close()
            print("wait_for_mysql: ok")
            return 0
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            time.sleep(1)

    print(f"wait_for_mysql: timed out: {last_err}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
