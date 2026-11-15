#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/13 15:42
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   nodes.py
# @Desc     :

from typing import cast

from langgraph.runtime import Runtime

from ..models import ACWRAssessment
from .services import ACWRCalculator
from .states import Context, Input, Output, State


def node_calculate(state: Input, runtime: Runtime[Context]) -> State:
    """
    The node for calculating the statistics

    :param state: Input state
    :param runtime: Runtime context
    :return: State
    """
    runtime.context.logs.append(state.status)

    with ACWRCalculator(state.data) as calculator:
        outcome = calculator.calculate()

    runtime.context.logs.append("Calculation")
    return State(statistics=outcome)


def node_assess(state: State, runtime: Runtime[Context]) -> Output:
    """
    The note for assessing the statistics

    :param state: State
    :param runtime: Runtime context
    :return: Output
    """
    structured_llm = runtime.context.agent.with_structured_output(
        ACWRAssessment,
        method=runtime.context.method.JSON_SCHEMA.value
    )
    outcome = cast(
        ACWRAssessment,
        structured_llm.invoke(runtime.context.prompt.invoke({
            "statistics": state.statistics,
            "language": runtime.context.language,
        }))
    )

    runtime.context.logs.append("Assessment")
    runtime.context.logs.append("End")
    return Output(assessment=outcome)
