#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/12 22:33
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   prompts.py
# @Desc     :

from typing import Self

from pandas import DataFrame

from utils.helper import Access


class ACWRCalculator(Access):
    """ ACWR Calculator Service """

    def __init__(self, acwr_data: DataFrame) -> None:
        """ Initialize the ACWRCalculator with ACWR data """
        self._data = acwr_data.sort_values("date").copy()

    @staticmethod
    def _prepare() -> list[str]:
        """ Prepare the data for analysis """
        return [
            "obj_training_load",
            "sub_training_load",
            "obj_acute",
            "sub_acute",
            "obj_chronic",
            "sub_chronic",
            "obj_acwr",
            "sub_acwr",
            "difference",
        ]

    def calculate(self) -> dict[str, dict[str, float]]:
        """ Analyse the ACWR data """
        _columns = self._prepare()

        _result: dict[str, dict[str, float]] = {}

        for col in _columns:
            series = self._data[col].dropna()

            if series.empty:
                continue

            _result[col] = {
                "latest": float(series.iloc[-1]),
                "mean": float(series.mean()),
                "min": float(series.min()),
                "max": float(series.max()),
                "trend": (float(series.iloc[-1] - series.iloc[0]) if len(series) > 1 else 0.0),
            }
        return _result

    def __enter__(self) -> Self:
        """ Enter the context manager. """
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """ Exit the context manager. """
        pass
