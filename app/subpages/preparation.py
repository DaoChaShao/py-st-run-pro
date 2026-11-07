#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/7 15:20
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   preparation.py
# @Desc     :   

from pathlib import Path

from sqlalchemy import func
from streamlit import empty, sidebar, rerun

from utils.dbk import (
    DBConfig,
    eliminate_db,
    InitEngine,
    drop_db,
    InitSession,
    create_db,
    Exercise,
    count_exercises,
)

MESSAGES = empty()

BASE = Path(__file__).resolve().parents[2]
SQLITE: Path = BASE / "data/sqlite3.db"
config: DBConfig = DBConfig(path=SQLITE)
sqlite = InitEngine(config)

if SQLITE.exists():
    with InitSession(sqlite.engine).init() as session:
        count = count_exercises(session, Exercise)
        MESSAGES.info(f"SQLite database found. Number of exercises: {count}")

    if sidebar.button("New Exercise", type="primary", width="stretch"):
        # with InitSession(sqlite.engine).init() as session:
        #     for _ in range(1):
        #         exercise = Exercise(
        #             date=date_date(2026, 9, 9),
        #             time=date_time(9, 45),
        #             week="Wed",
        #             type="J",
        #
        #             slope=3,
        #             duration=date_time(0, 37, 50),
        #             distance=5.61,
        #             active_calories=440,
        #             total_calories=514,
        #             avg_cadence=163,
        #             avg_pace=date_time(0, 6, 44),
        #             avg_heart_rate=152,
        #             effort=6,
        #
        #             zone_i=date_time(0, 0, 42),
        #             zone_ii=date_time(0, 2, 52),
        #             zone_iii=date_time(0, 13, 18),
        #             zone_iv=date_time(0, 21, 00),
        #             zone_v=date_time(0, 0, 00),
        #
        #             post_heart_rate_i=159,
        #             post_heart_rate_ii=143,
        #             post_heart_rate_iii=136,
        #         )
        #         session.add(exercise)
        #     session.commit()
        pass

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
