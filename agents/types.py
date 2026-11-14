#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/12 21:59
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   types.py
# @Desc     :

from enum import StrEnum, unique


@unique
class ModelCategories(StrEnum):
    DEEPSEEK = "DeepSeek"
    OPENAI = "OpenAI"


@unique
class ModelOutputMethods(StrEnum):
    FUNCTION_CALLING = "function_calling"
    JSON_MODE = "json_mode"
    JSON_SCHEMA = "json_schema"
