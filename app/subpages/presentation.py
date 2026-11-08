#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/8 13:41
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   presentation.py
# @Desc     :

from streamlit import (
    empty,
    stop,
)

from app.tools import CONFIG, SQLITE, check_db_status_with_stop
from utils.dbk import Exercise, InitEngine, InitSession, count_data

NOTIFICATION = empty()

sqlite = InitEngine(CONFIG)

if not check_db_status_with_stop(SQLITE, sqlite.engine, Exercise.__tablename__, NOTIFICATION):
    stop()

with InitSession(sqlite.engine).init() as session:
    count = count_data(session, Exercise)

    if count == 0:
        NOTIFICATION.info("SQLite database found, but no exercises recorded yet.")
    else:
        NOTIFICATION.success(f"QLite database found. Total exercises: {count}")
