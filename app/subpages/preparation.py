#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/7 15:20
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   preparation.py
# @Desc     :


from streamlit import (
    data_editor,
    empty,
    rerun,
    sidebar,
)

from app.tools import CONFIG, SQLITE, check_delete, new_exercise
from utils.dbk import (
    Exercise,
    InitEngine,
    InitSession,
    count_data,
    create_db,
    drop_db,
    eliminate_db,
    get_data,
)

MESSAGES = empty()

sqlite = InitEngine(CONFIG)

if SQLITE.exists():
    with InitSession(sqlite.engine).init() as session:
        count = count_data(session, Exercise)

        if count == 0:
            MESSAGES.info("SQLite database found, but no exercises recorded yet.")
        else:
            MESSAGES.success(f"QLite database found. Total exercises: {count}")
            data_editor(get_data(session, Exercise), hide_index=True, disabled=True, width="stretch")

    if sidebar.button("New Exercise", type="primary", width="stretch"):
        new_exercise(sqlite.engine, Exercise)

    if sidebar.button("Delete All Data", type="secondary", width="stretch", disabled=False):
        check_delete(sqlite.engine, Exercise)

    if sidebar.button("Drop All Tables", type="secondary", width="stretch", disabled=True):
        drop_db(sqlite.engine)
        rerun()

    if sidebar.button("Eliminate Database", type="tertiary", width="stretch"):
        eliminate_db(sqlite.engine, SQLITE)
        rerun()
else:
    MESSAGES.error("SQLite database not found. Please Initialise it initially.")
    if sidebar.button("Initialise Database", type="primary", width="stretch"):
        create_db(sqlite.engine)
        rerun()
