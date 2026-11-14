#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/10 15:08
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   acwr.py
# @Desc     :

from pandas import DataFrame
from streamlit import (
    data_editor,
    empty,
    expander,
    line_chart,
    markdown,
    rerun,
    session_state,
    sidebar,
    spinner,
)

from agents import ACWRAssessment, ACWRGrapher
from app.tools import CONFIG, check_api_key
from utils.dbk import InitEngine

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

        markdown("##### Acute:Chronic Workload Ratio Data & Chart")
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

        sidebar.divider()
        providers: list[str] = ["OpenAI", "DeepSeek"]
        provider: str = sidebar.selectbox(
            "Select a Large Language Model", ["Select a model"] + providers, index=0,
            help="Choose a large language model to be used for data analysis."
        )
        header: str = ""
        models: list[str] = []
        if provider != "Select a model":
            sidebar.caption(f"The model you selected is **{provider}**.")
            match provider:
                case "OpenAI":
                    header = "OpenAI Parameters"
                    models: list[str] = ["gpt-5.5-2026-04-23", "gpt-5.6-terra", "gpt-6-sol"]
                case "DeepSeek":
                    header = "DeepSeek Parameters"
                    models: list[str] = ["deepseek-v4-flash", "deepseek-v4-pro"]
                case _:
                    raise ValueError("Invalid model")

            sidebar.subheader(header)
            language: str = sidebar.selectbox(
                "Language", options=["English", "Chinese"], index=0,
                help="Select the language to use for the analysis."
            )
            temperature: float = sidebar.slider(
                "Temperature",
                min_value=0.0, max_value=2.0, step=0.1, disabled=True, value=0.0,
                help="Controls the randomness of the model's output. Lower values make it more deterministic.",
            )
            model: str = sidebar.selectbox(
                "Model", options=models,
                index=0, disabled=False,
                help="Select the OpenAI model to use.",
            )
            api_key: str = sidebar.text_input(
                "API Key",
                max_chars=164, type="password",
                placeholder="Enter your API key", help="Model API key for authentication",
            )
            if api_key:
                sidebar.caption(f"The length of API key you entered is {len(api_key)} characters.")
                check_api_key(api_key, model=provider, notification=NOTIFICATION)

                if sidebar.button("Generate AI Assessment", type="primary", width="stretch"):
                    agent_cols: list[str] = [
                        "date",
                        "obj_training_load", "sub_training_load",
                        "obj_acute", "sub_acute",
                        "obj_chronic", "sub_chronic",
                        "obj_acwr", "sub_acwr",
                        "difference",
                    ]
                    agent_data: DataFrame = session_state["ACWR"][agent_cols]

                    with (
                        spinner("Generating AI assessment...", show_time=True, width="stretch"),
                        ACWRGrapher(
                            agent_data,
                            model=provider,
                            temperature=temperature,
                            api_key=api_key,
                            language=language,
                        ) as grapher,
                    ):
                        response = grapher.graph()
                        # print(response)

                    assessment: ACWRAssessment = response["assessment"]

                    markdown("##### Training Analysis")
                    markdown(assessment.analysis)

                    markdown("##### Training Prescription")
                    markdown(assessment.prescription)

                    NOTIFICATION.success("AI assessment generated successfully.")
