#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/12 21:59
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   models.py
# @Desc     :

from pydantic import BaseModel, Field


class ACWRAssessment(BaseModel):
    analysis: str = Field(description="Training workload and fatigue analysis")
    prescription: str = Field(description="Training and recovery recommendations")
