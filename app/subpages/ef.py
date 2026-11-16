#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/12 16:51
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   ef.py
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

from agents import EFAssessment, EFGrapher
from app.tools import check_api_key

NOTIFICATION = empty()

for key in ["IMPUTATION", "DATA", "EF_ASSESSMENT", "EF_LOGS"]:
    if key not in session_state:
        session_state[key] = None

if session_state["IMPUTATION"] is None:
    NOTIFICATION.warning("Please perform imputation first.")
else:
    agent_cols: list[str] = [
        "date",
        "distance",
        "duration",
        "avg_heart_rate",
        "efficiency_factor",
    ]

    if session_state["DATA"] is None:
        NOTIFICATION.warning("Please load the data first.")

        if sidebar.button("Efficiency Factor View", type="primary", width="stretch"):
            session_state["DATA"] = session_state["IMPUTATION"][agent_cols].copy()
            rerun()
    else:
        NOTIFICATION.info("Data loaded successfully.")

        markdown("##### Efficiency Factor Data & Chart")
        with expander("**Efficiency Factor Data**", expanded=False):
            data_editor(session_state["DATA"], hide_index=True, disabled=True, width="stretch")

        chart_selection: list[str] = ["date", "efficiency_factor"]
        chart_data = session_state["DATA"][chart_selection].set_index("date").sort_index()
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

                if session_state["EF_ASSESSMENT"] is None or session_state["EF_LOGS"] is None:

                    if sidebar.button("Generate AI Assessment", type="primary", width="stretch"):
                        with (
                            spinner("Generating AI assessment...", show_time=True, width="stretch"),
                            EFGrapher(
                                session_state["DATA"].copy(),
                                model=provider,
                                temperature=temperature,
                                api_key=api_key,
                                language=language,
                            ) as grapher,
                        ):
                            response, session_state["EF_LOGS"] = grapher.graph()
                            # print(response)

                        session_state["EF_ASSESSMENT"]: EFAssessment = response["assessment"]
                        rerun()
                else:
                    with expander("**AI Graph Logs**", expanded=False):
                        write(session_state["EF_LOGS"])

                    markdown("##### Training Analysis")
                    markdown(session_state["EF_ASSESSMENT"].analysis)
                    markdown("##### Training Prescription")
                    markdown(session_state["EF_ASSESSMENT"].prescription)

                    NOTIFICATION.success("AI assessment generated successfully.")

                    if sidebar.button("Regenerate AI Assessment", type="secondary", width="stretch"):
                        session_state["EF_ASSESSMENT"] = None
                        session_state["EF_LOGS"] = None
                        rerun()
