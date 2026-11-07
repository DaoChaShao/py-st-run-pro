#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/7 15:20
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   preparation.py
# @Desc     :

from pandas import DataFrame
from streamlit import (
    dataframe,
    empty,
    rerun,
    sidebar,
)

from app.tools import (
    CONFIG,
    SQLITE,
    create_data,
    delete_all_data,
    delete_all_tables,
    delete_db,
    delete_selected_data,
    update_data,
)
from utils.dbk import (
    Exercise,
    InitEngine,
    InitSession,
    check_table_exists,
    count_data,
    create_db,
    get_data,
)

MESSAGES = empty()

sqlite = InitEngine(CONFIG)

if not SQLITE.exists():
    MESSAGES.error("SQLite database not found.")
    if sidebar.button("Initialise Database", type="primary", width="stretch"):
        create_db(sqlite.engine)
        rerun()

elif not check_table_exists(sqlite.engine, Exercise.__tablename__):
    MESSAGES.warning("SQLite database found, but table not found.")
    if sidebar.button("Initialise Database", type="primary", width="stretch"):
        create_db(sqlite.engine)
        rerun()
else:
    with InitSession(sqlite.engine).init() as session:
        count = count_data(session, Exercise)

        if count == 0:
            MESSAGES.info("SQLite database found, but no exercises recorded yet.")
        else:
            MESSAGES.success(f"QLite database found. Total exercises: {count}")

            exercises: DataFrame = get_data(session, Exercise)
            selection = dataframe(
                exercises,
                hide_index=True, width="stretch",
                selection_mode="single-row",
                on_select="rerun",
            )

            selected_row = selection.get("selection", {}).get("rows", [])
            if len(selected_row) > 0:
                # print(selected_row)
                df_idx = selected_row[0]
                db_idx = int(exercises.iloc[df_idx]["id"])
                # print(f"Dataframe index: {df_idx}, Database index: {db_idx}, Database index type: {type(db_idx)}")

                if sidebar.button("Update Selected Data", type="secondary", width="stretch"):
                    update_data(sqlite.engine, Exercise, db_idx)

                if sidebar.button("Delete This Data", type="tertiary", width="stretch"):
                    delete_selected_data(sqlite.engine, Exercise, db_idx)
            else:
                # print(selected_row)
                pass

    if sidebar.button("New Exercise", type="primary", width="stretch"):
        create_data(sqlite.engine, Exercise)

    if sidebar.button("Delete All Data", type="secondary", width="stretch", disabled=False):
        delete_all_data(sqlite.engine, Exercise)

    if sidebar.button("Drop All Tables", type="secondary", width="stretch", disabled=False):
        delete_all_tables(sqlite.engine)

    sidebar.divider()
    if sidebar.button("Eliminate Database", type="tertiary", width="stretch"):
        delete_db(sqlite.engine, SQLITE)
