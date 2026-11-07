#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/7 15:09
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   __init__.py.py
# @Desc     :

"""
****************************************************************
Tools for Streamlit Application
----------------------------------------------------------------
A collection of utility tools designed for Streamlit page initialisation and core function execution.
****************************************************************
"""

__author__ = "Shawn Yu"
__version__ = "0.1.0"

from .hammer import CONFIG, SQLITE, check_delete, new_exercise
from .layout import config_page, set_pages

__all__ = [
    "CONFIG",
    "SQLITE",
    "check_delete",
    "new_exercise",

    "config_page",
    "set_pages",
]
