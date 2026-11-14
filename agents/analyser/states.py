#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/13 15:39
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   states.py
# @Desc     :

from operator import add
from typing import Annotated

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from pandas import DataFrame
from pydantic import BaseModel, ConfigDict

from utils.types import Languages

from ..types import ModelOutputMethods
from .models import ACWRAssessment


class State(BaseModel):
    """ Main State"""
    status: str
    logs: Annotated[list[str], add]
    statistics: dict[str, dict[str, float]]


class Context(BaseModel):
    """ Context State """
    agent: BaseChatModel
    prompt: ChatPromptTemplate
    method: ModelOutputMethods = ModelOutputMethods.JSON_SCHEMA
    language: Languages = Languages.EN


class Input(BaseModel):
    """ Input State """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    status: str
    data: DataFrame


class Output(BaseModel):
    """ Output State """
    status: str
    assessment: ACWRAssessment
