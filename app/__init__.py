#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/7 15:07
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   __init__.py.py
# @Desc     :

"""
****************************************************************
Streamlit Application Package
----------------------------------------------------------------
This package provides:

+ subpages: All Streamlit subpage modules (home, etc.).
+ tools: Page configuration, layout control, and navigation utilities.

It serves as the entry point for loading app modules and exposing
core subpackages for high-level import and integration.
****************************************************************
"""

__author__ = "Shawn Yu"
__version__ = "0.1.0"

from . import subpages, tools

__all__ = [
    "subpages",
    "tools",
]
