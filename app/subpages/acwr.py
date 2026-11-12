#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/10 15:08
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   acwr.py
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

for key in ["EXERCISES", "ACWR"]:
    if key not in session_state:
        session_state[key] = None

if session_state["EXERCISES"] is None:
    NOTIFICATION.warning("Please load the data first.")
else:
    data = session_state["EXERCISES"].copy()
    NOTIFICATION.info("Data loaded successfully.")

    if session_state["ACWR"] is None:

        if sidebar.button("Calculate ACWR", type="primary", width="stretch"):
            # Calculate the training load
            data["obj_training_load"] = data["effort"] * data["duration"]
            data["sub_training_load"] = data["rpe"] * data["duration"]

            # Aggregate daily training load
            obj_daily = data.groupby(data["date"].dt.normalize())["obj_training_load"].sum().resample("D").sum()
            sub_daily = data.groupby(data["date"].dt.normalize())["sub_training_load"].sum().resample("D").sum()

            # Calculate the acute:chronic workload ratio
            dates = data["date"].dt.normalize()

            data["obj_acute"] = dates.map(obj_daily.rolling(window=7, min_periods=7).sum())
            data["obj_chronic"] = dates.map(obj_daily.rolling(window=28, min_periods=28).sum() / 4)
            data["obj_acwr"] = data["obj_acute"] / (data["obj_chronic"] + 1e-5)

            data["sub_acute"] = dates.map(sub_daily.rolling(window=7, min_periods=7).sum())
            data["sub_chronic"] = dates.map(sub_daily.rolling(window=28, min_periods=28).sum() / 4)
            data["sub_acwr"] = data["sub_acute"] / (data["sub_chronic"] + 1e-5)

            data["difference"] = data["obj_acwr"] - data["sub_acwr"]

            session_state["ACWR"] = data
            rerun()
    else:
        NOTIFICATION.success("ACWR calculated successfully.")
        with expander("**Training Load Data**", expanded=False):
            data_editor(session_state["ACWR"], hide_index=True, disabled=True, width="stretch")

        days: int = (
                            session_state["ACWR"]["date"].max().normalize()
                            - session_state["ACWR"]["date"].min().normalize()
                    ).days + 1
        diff: list[str] = []
        if days < 7:
            objs = ["obj_training_load"]
            subs = ["sub_training_load"]
        elif days < 28:
            objs = ["obj_acute"]
            subs = ["sub_acute"]
        else:
            objs = ["obj_acwr"]
            subs = ["sub_acwr"]
            diff = ["difference"]

        category: str = sidebar.selectbox(
            "Select the ACWR category to display:",
            options=["Objective Workload", "Subjective Workload", "Comparison"], index=0,
            width="stretch", help="Select the ACWR category to display."
        )
        match category:
            case "Objective Workload":
                options = objs
            case "Subjective Workload":
                options = subs
            case "Comparison":
                options = objs + subs + diff
            case _:
                raise ValueError("Invalid category")
        selections: list[str] = sidebar.multiselect(
            "Select the workload metrics to display:",
            options=options, default=options, disabled=False,
            width="stretch", help="Select the workload metrics to display."
        )
        if selections:
            chart_data = session_state["ACWR"].set_index("date").sort_index()[selections]
            # with FeatureScaler(chart_data, category=FeatureScalers.NORMALISATION) as scaler:
            #     scaled_data = scaler.scale()
            line_chart(chart_data, width="stretch")
