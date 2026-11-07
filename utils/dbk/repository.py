#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/7 16:00
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   repository.py
# @Desc     :

from typing import Any

from pandas import DataFrame, read_sql
from sqlalchemy.orm import Session
from sqlalchemy.sql import func


def count_data(session: Session, table: Any) -> int:
    """ Count the number of the table in the database """
    return session.query(func.count(table.id)).scalar()


def delete_data(session: Session, table: Any) -> None:
    """ Delete the data in the table """
    session.query(table).delete()
    session.commit()


def get_data(session: Session, table: Any) -> DataFrame:
    """ Get the data from the table """
    statement = session.query(table).statement
    return read_sql(statement, session.bind)
