#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/8 13:41
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   presentation.py
# @Desc     :

from pandas import DataFrame
from streamlit import (
    empty,
    stop,
    selectbox,
    line_chart,
    columns,
    metric,
    sidebar,
)

from app.tools import CONFIG, SQLITE, check_db_status_with_stop
from utils.dbk import Exercise, InitEngine, InitSession, count_data, get_data

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

        exercises: DataFrame = get_data(session, Exercise)

        left, right = columns(2)
        all_values: int = exercises.size
        dup_values: int = exercises.duplicated().sum()
        mis_values: int = exercises.isnull().sum().sum()
        with left:
            metric(
                "Duplicate values", value=dup_values,
                delta=all_values - dup_values,
                delta_color="normal" if all_values - dup_values >= all_values else "inverse",
                help="Number of duplicate rows in the dataset"
            )
        with right:
            metric(
                "Missing values", value=mis_values,
                delta=all_values - mis_values,
                delta_color="normal" if all_values - mis_values >= all_values else "inverse",
                help="Number of missing values in the dataset"
            )

        if dup_values != 0 or mis_values != 0:
            if sidebar.button("Data Imputation", type="primary", width="stretch"):
                pass
        else:
            # Calculate Efficiency Factor
            exercises["efficiency_factor"] = (
                    (exercises["distance"] / (exercises["duration"] / 60)) / exercises["avg_heart_rate"]
            )
            exercises["stride_length"] = (
                    (exercises["distance"] * 1000) / (exercises["avg_cadence"] * exercises["duration"])
            )

            cols: list[str] = exercises.columns.tolist().copy()
            removal: list[str] = ["id", "date", "time", "week", "type", "create_date", "update_date"]
            selections: list[str] = [col for col in cols if col not in removal]

            selection: str = selectbox(
                "Overall Trend", options=selections, index=0,
                width="stretch", help="Select a column to display"
            )

            data = exercises[["date", selection]].set_index("date")
            line_chart(data, width="stretch", height="stretch")
