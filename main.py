#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/10/21 19:16
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   main.py
# @Desc     :

from pathlib import Path

from utils.dbk import DBConfig, InitializeEngine, create_database, eliminate_database


def main() -> None:
    """ Main Function """
    # filepath: Path = Path("data/exercise.xlsx")
    # with TabularLoader(filepath, display=True) as loader:
    #     exercises: DataFrame = loader.load(file_category=TabularFormats.EXCEL)

    db_path: Path = Path("data/sqlite3.db")
    config: DBConfig = DBConfig(path=db_path)
    sqlite = InitializeEngine(config)

    create_database(sqlite.engine)

    # eliminate_database(sqlite.engine, db_path)


if __name__ == "__main__":
    main()
