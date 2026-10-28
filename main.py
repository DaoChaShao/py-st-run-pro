#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/10/21 19:16
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   main.py
# @Desc     :

from pathlib import Path

from pandas import DataFrame

from utils.stats import TabularFormats, TabularLoader


def main() -> None:
    """ Main Function """
    filepath: Path = Path("data/exercise.xlsx")
    with TabularLoader(filepath, display=True) as loader:
        exercises: DataFrame = loader.load(file_category=TabularFormats.EXCEL)


if __name__ == "__main__":
    main()
