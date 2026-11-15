#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/13 15:39
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   states.py
# @Desc     :


from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from pandas import DataFrame
from pydantic import BaseModel, Field, InstanceOf

from utils.types import Languages

from ..models import ACWRAssessment
from ..types import ModelOutputMethods


class State(BaseModel):
    """ Main State"""
    statistics: dict[str, dict[str, float]]


class Context(BaseModel):
    """ Context State """
    agent: BaseChatModel
    prompt: ChatPromptTemplate
    method: ModelOutputMethods = ModelOutputMethods.JSON_SCHEMA
    language: Languages = Languages.EN
    logs: list[str] = Field(default_factory=list)


class Input(BaseModel):
    """ Input State

    - str
    - int
    - float
    - bool
    - list
    - dict
    """
    status: str
    # Method I
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    # Method II
    data: InstanceOf[DataFrame]


class Output(BaseModel):
    """ Output State """
    assessment: ACWRAssessment
