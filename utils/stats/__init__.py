#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/10/21 19:41
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   __init__.py.py
# @Desc     :

"""
****************************************************************
Data Processing Module - Comprehensive Toolkit
----------------------------------------------------------------
This module provides a comprehensive suite of data analysis functions
and classes designed for general data processing tasks.
****************************************************************
"""

__author__ = "Shawn Yu"
__version__ = "0.1.0"

from .lever import NumpySeed, summary_dataframe
from .preprocessor import (
    TabularLoader,
    get_cls_label_distribution,
    get_reg_label_distribution,
)
from .types import (
    TabularFormats,
)

__all__ = [
    "NumpySeed",
    "summary_dataframe",

    "TabularLoader",
    "get_cls_label_distribution", "get_reg_label_distribution",

    "TabularFormats",
]
