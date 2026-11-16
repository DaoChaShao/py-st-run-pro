#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/16 18:18
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   nodes.py
# @Desc     :

from typing import cast

from langgraph.runtime import Runtime

from ..models import HRRAssessment
from .states import HRRContext, HRRInput, HRROutput


def hrr_node_assess(state: HRRInput, runtime: Runtime[HRRContext]) -> HRROutput:
    """
    The note for assessing the Efficiency Factor

    :param state: State
    :param runtime: Runtime context
    :return: Output
    """
    runtime.context.logs.append(state.status)
    structured_llm = runtime.context.agent.with_structured_output(
        HRRAssessment,
        method=runtime.context.method.JSON_SCHEMA.value
    )
    outcome = cast(
        HRRAssessment,
        structured_llm.invoke(runtime.context.prompt.invoke({
            "data": state.data,
            "language": runtime.context.language,
        }))
    )

    runtime.context.logs.append("Assessment")
    runtime.context.logs.append("End")
    return HRROutput(assessment=outcome)
