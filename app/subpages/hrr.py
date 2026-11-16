#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/16 17:13
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   hrr.py
# @Desc     :

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
    write,
)

from agents import HRRAssessment, HRRGrapher
from app.tools import cal_hrr, check_api_key

NOTIFICATION = empty()

for key in ["IMPUTATION", "HRR", "HRR_ASSESSMENT", "HRR_LOGS"]:
    if key not in session_state:
        session_state[key] = None

if session_state["IMPUTATION"] is None:
    NOTIFICATION.warning("Please perform imputation first.")
else:
    NOTIFICATION.info("Heart Rate Recovery analysis not yet implemented.")

    if session_state["HRR"] is None:
        hrr_cols: list[str] = [
            "date",
            "post_heart_rate_i",
            "post_heart_rate_ii",
            "post_heart_rate_iii",
        ]

        if sidebar.button("Calculate HRR", type="primary", width="stretch"):
            data = session_state["IMPUTATION"].copy()[hrr_cols]
            session_state["HRR"] = cal_hrr(data)
            rerun()
    else:
        NOTIFICATION.success("Heart Rate Recovery analysis completed.")

        markdown("##### Heart Rate Recovery Data & Chart")
        with expander("**Heart Rate Recovery Data**", expanded=False):
            data_editor(session_state["HRR"], hide_index=True, disabled=True, width="stretch")

        options: list[str] = [
            "hr_drop_0_1_min",
            "hr_drop_0_2_min",
            "hr_drop_1_2_min",
        ]
        chart_selections: list[str] = sidebar.multiselect(
            "Select columns to plot",
            options=options, default=options, disabled=False,
            width="stretch", help="Select the columns to plot"
        )
        chart_data = session_state["HRR"].set_index("date").sort_index()[chart_selections]
        line_chart(chart_data, width="stretch", height="stretch")

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

                if session_state["HRR_ASSESSMENT"] is None or session_state["HRR_LOGS"] is None:

                    if sidebar.button("Generate AI Assessment", type="primary", width="stretch"):
                        with (
                            spinner("Generating AI assessment...", show_time=True, width="stretch"),
                            HRRGrapher(
                                session_state["HRR"].copy(),
                                model=provider,
                                temperature=temperature,
                                api_key=api_key,
                                language=language,
                            ) as grapher,
                        ):
                            response, session_state["HRR_LOGS"] = grapher.graph()
                            # print(response)

                        session_state["HRR_ASSESSMENT"]: HRRAssessment = response["assessment"]
                        rerun()
                else:
                    with expander("**AI Graph Logs**", expanded=False):
                        write(session_state["HRR_LOGS"])

                    markdown("##### Training Analysis")
                    markdown(session_state["HRR_ASSESSMENT"].analysis)
                    markdown("##### Training Prescription")
                    markdown(session_state["HRR_ASSESSMENT"].prescription)

                    NOTIFICATION.success("AI assessment generated successfully.")

                    if sidebar.button("Regenerate AI Assessment", type="secondary", width="stretch"):
                        session_state["HRR_ASSESSMENT"] = None
                        session_state["HRR_LOGS"] = None
                        rerun()
