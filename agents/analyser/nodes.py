#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/13 15:42
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   nodes.py
# @Desc     :

from typing import cast

from langgraph.runtime import Runtime

from .models import ACWRAssessment
from .services import ACWRCalculator
from .states import Context, Input, Output, State


def node_calculate(state: Input) -> State:
    """ Calculate the notes """
    curr_status: str = "Calculation"
    with ACWRCalculator(state.data) as calculator:
        outcome = calculator.calculate()
    return State(status=curr_status, statistics=outcome, logs=[curr_status])


def node_assess(state: State, runtime: Runtime[Context]) -> Output:
    """ Assess the notes """
    structured_llm = runtime.context.agent.with_structured_output(ACWRAssessment, method="json_schema")
    outcome = cast(
        ACWRAssessment,
        structured_llm.invoke(runtime.context.prompt.invoke({
            "statistics": state.statistics,
            "language": runtime.context.language,
        }))
    )
    return Output(status="Assessment", assessment=outcome)
