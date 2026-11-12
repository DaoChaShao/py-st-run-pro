#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/12 16:51
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   ef.py
# @Desc     :

from streamlit import (
    empty,
    session_state,
)

from app.tools import CONFIG
from utils.dbk import InitEngine

NOTIFICATION = empty()

sqlite = InitEngine(CONFIG)

for key in ["EXERCISES", ]:
    if key not in session_state:
        session_state[key] = None

if session_state["EXERCISES"] is None:
    NOTIFICATION.warning("Please load the data first.")
else:
    data = session_state["EXERCISES"].copy()
    NOTIFICATION.info("Data loaded successfully.")
