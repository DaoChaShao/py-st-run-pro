#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/8 13:41
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   preparation.py
# @Desc     :

from streamlit import (
    columns,
    data_editor,
    date_input,
    empty,
    expander,
    line_chart,
    markdown,
    metric,
    rerun,
    session_state,
    sidebar,
    stop,
)

from app.tools import (
    CONFIG,
    GROUPS,
    SQLITE,
    cal_efficiency_factor,
    cal_stride_length,
    check_db_status_with_stop,
    map_col_labels,
)
from utils.dbk import (
    Exercise,
    InitEngine,
    InitSession,
    count_data,
    get_data,
)
from utils.stats import DataImputer, FeatureScaler, FeatureScalers

NOTIFICATION = empty()

sqlite = InitEngine(CONFIG)

for key in ["EXERCISES"]:
    if key not in session_state:
        session_state[key] = None

if not check_db_status_with_stop(SQLITE, sqlite.engine, Exercise.__tablename__, NOTIFICATION):
    stop()

with InitSession(sqlite.engine).init() as session:
    count = count_data(session, Exercise)

    if count == 0:
        NOTIFICATION.info("SQLite database found, but no exercises recorded yet.")
    else:
        NOTIFICATION.success(f"QLite database found. Total exercises: {count}")

        if session_state["EXERCISES"] is None:
            session_state["EXERCISES"] = get_data(session, Exercise).copy()

        markdown("##### Data Overview")
        left, right = columns(2)
        all_values: int = session_state["EXERCISES"].size
        dup_values: int = session_state["EXERCISES"].duplicated().sum()
        mis_values: int = session_state["EXERCISES"].isnull().sum().sum()
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
                with DataImputer(session_state["EXERCISES"]) as imputer:
                    imputer.impute()
                rerun()
        else:
            # Calculate Efficiency Factor
            session_state["EXERCISES"] = cal_efficiency_factor(session_state["EXERCISES"])
            # Calculate Stride Length
            session_state["EXERCISES"] = cal_stride_length(session_state["EXERCISES"])

            cols: list[str] = session_state["EXERCISES"].columns.tolist().copy()
            removal: list[str] = ["id", "date", "time", "week", "type", "create_date", "update_date"]
            selections: list[str] = [col for col in cols if col not in removal]
            # print(selections)

            selection: str = sidebar.selectbox(
                "Overall Trend", options=selections, index=0,
                width="stretch", format_func=map_col_labels,
                help="Select a column to display"
            )
            sidebar.caption("The selected column will be displayed as a line chart on the right.")

            with expander("**Imputation Data**", expanded=False):
                data_editor(session_state["EXERCISES"], hide_index=True, disabled=True, width="stretch")

            markdown("##### Overall Line Chart")
            selected_data = session_state["EXERCISES"][["date", selection]].set_index("date").sort_index()
            start, end = columns(2)
            with start:
                start_date = date_input(
                    "Start Date",
                    min_value=selected_data.index.min().date(),
                    max_value=selected_data.index.max().date(),
                    value=selected_data.index.min().date(),
                    width="stretch", help="Select the start date for the chart",
                )
            with end:
                end_date = date_input(
                    "End Date",
                    min_value=start_date, max_value=selected_data.index.max().date(),
                    value=selected_data.index.max().date(),
                    width="stretch", help="Select the end date for the chart",
                )

            overall_data = selected_data.loc[start_date.isoformat():end_date.isoformat()]
            line_chart(overall_data, width="stretch", height="stretch")

            markdown("##### Grouped Line Chart")
            group: str = sidebar.selectbox("Chart Group", options=list(GROUPS))
            sidebar.caption(GROUPS[group]["description"])
            picks: list[str] = sidebar.multiselect(
                "Metrics",
                options=GROUPS[group]["columns"],
                default=GROUPS[group]["columns"],
                format_func=map_col_labels,
            )

            if picks:
                grouped_data = session_state["EXERCISES"][["date", *picks]].set_index("date").sort_index()
                with FeatureScaler(grouped_data, category=FeatureScalers.NORMALISATION) as scaler:
                    grouped_data = scaler.scale()

                grouped_data = grouped_data.loc[start_date.isoformat():end_date.isoformat()]
                line_chart(grouped_data, width="stretch", height="stretch")
