#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/7 16:00
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   repository.py
# @Desc     :   

from typing import Any

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import func


def count_exercises(session: Session, table: Any) -> int:
    return session.query(func.count(table.id)).scalar()
