#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/10/21 19:16
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   main.py
# @Desc     :


from app.tools import config_page, set_pages


def main() -> None:
    """ streamlit run main.py """
    # filepath: Path = Path("data/exercise.xlsx")
    # with TabularLoader(filepath, display=True) as loader:
    #     exercises: DataFrame = loader.load(file_category=TabularFormats.EXCEL)

    # path: Path = Path("data/sqlite3.db")
    # config: DBConfig = DBConfig(path=path)
    # sqlite = InitEngine(config)
    #
    # # create_db(sqlite.engine)
    #
    # # eliminate_db(sqlite.engine, path)
    #
    # with InitSession(sqlite.engine).init() as session:
    #     for _ in range(1):
    #         exercise = Exercise(
    #             date=date_date(2026, 9, 9),
    #             time=date_time(9, 45),
    #             week="Wed",
    #             type="J",
    #
    #             slope=3,
    #             duration=date_time(0, 37, 50),
    #             distance=5.61,
    #             active_calories=440,
    #             total_calories=514,
    #             avg_cadence=163,
    #             avg_pace=date_time(0, 6, 44),
    #             avg_heart_rate=152,
    #             effort=6,
    #
    #             zone_i=date_time(0, 0, 42),
    #             zone_ii=date_time(0, 2, 52),
    #             zone_iii=date_time(0, 13, 18),
    #             zone_iv=date_time(0, 21, 00),
    #             zone_v=date_time(0, 0, 00),
    #
    #             post_heart_rate_i=159,
    #             post_heart_rate_ii=143,
    #             post_heart_rate_iii=136,
    #         )
    #         session.add(exercise)
    #     session.commit()

    config_page()
    set_pages()


if __name__ == "__main__":
    main()
