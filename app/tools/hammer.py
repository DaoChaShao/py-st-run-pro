#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/7 16:31
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   hammer.py
# @Desc     :

from datetime import date as date_date
from datetime import datetime, timedelta
from datetime import time as date_time
from os import remove
from pathlib import Path
from typing import Any

from pandas import DataFrame
from sqlalchemy.engine import Engine
from streamlit import (
    button,
    caption,
    columns,
    date_input,
    dialog,
    empty,
    number_input,
    rerun,
    segmented_control,
    selectbox,
    session_state,
    sidebar,
    slider,
    time_input,
)

from utils.dbk import (
    DECLARATION,
    DBConfig,
    InitSession,
    check_table_exists,
    create_db,
)
from utils.stats import TabularFormats, TabularLoader

BASE = Path(__file__).resolve().parents[2]
SQLITE: Path = BASE / "data/sqlite3.db"
EXCEL: Path = BASE / "data/exercise.xlsx"
CONFIG: DBConfig = DBConfig(path=SQLITE)

GROUPS: dict[str, dict[str, list | str]] = {
    "Exercise Volume & Pace": {
        "columns": ["distance", "duration", "avg_pace"],
        "description": "Analyses exercise volume, duration, and pacing performance."
    },
    "Heart Rate & Intensity": {
        "columns": ["avg_heart_rate", "effort", "rpe"],
        "description": "Evaluates cardiovascular workload and perceived exercise intensity."
    },
    "Heart Rate Recovery": {
        "columns": ["post_heart_rate_i", "post_heart_rate_ii", "post_heart_rate_iii"],
        "description": "Tracks post-exercise heart rate recovery patterns."
    },
    "Heart Rate Zones": {
        "columns": ["zone_i", "zone_ii", "zone_iii", "zone_iv", "zone_v"],
        "description": "Examines the distribution of exercise intensity across heart rate zones."
    },
    "Energy Expenditure": {
        "columns": ["active_kilocalories", "total_kilocalories"],
        "description": "Compares active and total energy expenditure during exercise."
    },
    "Gait & Movement Efficiency": {
        "columns": ["avg_cadence", "stride_length"],
        "description": "Analyses cadence and stride length to assess movement patterns."
    },
    "Exercise Efficiency": {
        "columns": ["efficiency_factor", "avg_pace", "avg_heart_rate"],
        "description": "Examines the relationship between exercise efficiency, pace, and cardiovascular response."
    },
    "Body Weight": {
        "columns": ["weight"],
        "description": "Tracks changes in body weight over time."
    },
    "Terrain Impact": {
        "columns": ["slope", "avg_pace", "avg_heart_rate"],
        "description": "Examines how terrain gradient relates to pace and cardiovascular workload."
    },
}


def check_db_status_with_init(filepath: Path, engine: Engine, table: str, notification: Any) -> bool:
    """
    Check the status of the database

    :param filepath: The path to the database file
    :param engine: The database engine
    :param table: The name of the table
    :param notification: The notification object
    :return: True if the database is ready, otherwise False
    """
    if not filepath.exists():
        notification.error("SQLite database not found.")
        if sidebar.button("Initialise Database", type="primary", width="stretch"):
            create_db(engine)
            rerun()
        return False

    elif not check_table_exists(engine, table):
        notification.warning("SQLite database found, but table not found.")
        if sidebar.button("Initialise Database", type="primary", width="stretch"):
            create_db(engine)
            rerun()
        return False
    return True


def check_db_status_with_stop(filepath: Path, engine: Engine, table: str, notification: Any) -> bool:
    """
    Check the status of the database with stop

    :param filepath: The path to the database file
    :param engine: The database engine
    :param table: The name of the table
    :param notification: The notification object
    :return: True if the database is ready, otherwise False
    """
    if not filepath.exists() or not check_table_exists(engine, table):
        notification.error("Database or table not found. Please initialize it in the preparation page.")
        return False
    return True


def cal_efficiency_factor(data: DataFrame) -> DataFrame:
    """ Calculate the efficiency factor of the exercise """
    data["efficiency_factor"] = (data["distance"] / (data["duration"] / 60)) / data["avg_heart_rate"]
    return data


def cal_stride_length(data: DataFrame) -> DataFrame:
    """ Calculate the stride length of the exercise """
    data["stride_length"] = (data["distance"] * 1000) / (data["avg_cadence"] * data["duration"])
    return data


@dialog("Create a new data", width="medium", position="center")
def create_data(engine: Engine, table: Any) -> None:
    """
    Add a new exercise

    :param engine: The database engine
    :param table: The table object
    :return: None
    """
    caption("Basic Information:")
    left, mid, right = columns(3)
    with left:
        date: date_date = date_input(
            "Exercise Date", value=date_date.today(),
            width="stretch", help="Select the exercise date."
        )
    with mid:
        time: date_time = time_input(
            "Exercise Time", value=date_time.min, step=timedelta(seconds=1),
            width="stretch", help="Select the exercise time."
        )
    with right:
        week: str = selectbox(
            "Exercise Week", options=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            width="stretch", help="Select the exercise week."
        )

    caption("Exercise Details:")
    desc, details = columns(2)
    with desc:
        category: str = segmented_control(
            "Exercise Category", options=["J", "R"], default="J", disabled=True,
            width="stretch", help="Select the exercise category."
        )
        slope: float = slider(
            "Exercise Slope", min_value=0.0, max_value=10.0, value=3.0, step=1.0,
            width="stretch", help="Select the exercise slope."
        )
        duration: float = number_input(
            "Exercise Duration", min_value=0.0, max_value=100.0, step=0.01, value=3.0,
            width="stretch", help="Select the exercise duration."
        )
        distance: float = number_input(
            "Exercise Distance", min_value=0.0, max_value=50.0, step=0.01, value=5.00,
            width="stretch", help="Select the exercise distance."
        )
        active_kilocalories: float = number_input(
            "Exercise Active Calories", min_value=0.0, max_value=1000.0, step=1.0,
            width="stretch", help="Select the exercise active calories."
        )
        total_kilocalories: float = number_input(
            "Exercise Total Calories", min_value=0.0, max_value=1000.0, step=1.0,
            width="stretch", help="Select the exercise total calories."
        )
        avg_cadence: int = slider(
            "Exercise Average Cadence", min_value=0, max_value=200, step=1,
            width="stretch", help="Select the exercise average cadence."
        )
        avg_pace: float = number_input(
            "Exercise Average Pace", min_value=0.0, max_value=50.0, step=0.01,
            width="stretch", help="Select the exercise average pace."
        )
        avg_heart_rate: int = slider(
            "Exercise Average Heart Rate", min_value=0, max_value=200, step=1,
            width="stretch", help="Select the exercise average heart rate."
        )
        effort: int = slider(
            "Exercise Effort", min_value=0, max_value=10, step=1,
            width="stretch", help="Select the exercise effort."
        )

    with details:
        zone_i: float = number_input(
            "Heart Rate Zone I", min_value=0.0, max_value=100.0, step=0.01,
            width="stretch", help="Select the exercise zone I."
        )
        zone_ii: float = number_input(
            "Heart Rate Zone II", min_value=0.0, max_value=100.0, step=0.01,
            width="stretch", help="Select the exercise zone II."
        )
        zone_iii: float = number_input(
            "Heart Rate Zone III", min_value=0.0, max_value=100.0, step=0.01,
            width="stretch", help="Select the exercise zone III."
        )
        zone_iv: float = number_input(
            "Heart Rate Zone IV", min_value=0.0, max_value=100.0, step=0.01,
            width="stretch", help="Select the exercise zone IV."
        )
        zone_v: float = number_input(
            "Heart Rate Zone V", min_value=0.0, max_value=100.0, step=0.01,
            width="stretch", help="Select the exercise zone V."
        )
        post_heart_rate_i: int = slider(
            "Post-Exercise Heart Rate I", min_value=0, max_value=200, step=1,
            width="stretch", help="Select the post-exercise heart rate Immediately."
        )
        post_heart_rate_ii: int = slider(
            "Post-Exercise Heart Rate II", min_value=0, max_value=200, step=1,
            width="stretch", help="Select the post-exercise heart rate after 1 minute."
        )
        post_heart_rate_iii: int = slider(
            "Post-Exercise Heart Rate III", min_value=0, max_value=200, step=1,
            width="stretch", help="Select the post-exercise heart rate after 2 minutes."
        )
        weight: float = number_input(
            "Exercise Weight", min_value=0.0, max_value=200.0, step=0.01,
            width="stretch", help="Select the exercise weight."
        )
        rpe: int = slider(
            "Training Intensity (RPE)", min_value=0, max_value=10, step=1,
            width="stretch", help="Select the training intensity (RPE)."
        )

    if button("Submit", type="primary", width="stretch"):
        with InitSession(engine).init() as session:
            exercise = table(
                date=date,
                time=time,
                week=week,
                type=category,

                slope=slope,
                duration=duration,
                distance=distance,
                active_kilocalories=active_kilocalories,
                total_kilocalories=total_kilocalories,
                avg_cadence=avg_cadence,
                avg_pace=avg_pace,
                avg_heart_rate=avg_heart_rate,
                effort=effort,

                zone_i=zone_i,
                zone_ii=zone_ii,
                zone_iii=zone_iii,
                zone_iv=zone_iv,
                zone_v=zone_v,

                post_heart_rate_i=post_heart_rate_i,
                post_heart_rate_ii=post_heart_rate_ii,
                post_heart_rate_iii=post_heart_rate_iii,

                weight=weight,

                rpe=rpe,
            )
            session.add(exercise)
            session.commit()
        rerun()


@dialog("Delete all data", width="small", position="center")
def delete_all_data(engine: Engine, table: Any) -> None:
    """
    Confirm whether to delete all data

    :param engine: The database engine
    :param table: The table object
    :return: None
    """
    caption("Would you like to delete all data?")

    left, right = columns(2)
    with left:
        if button("Yes", type="secondary", width="stretch"):
            with InitSession(engine).init() as session:
                session.query(table).delete()
                session.commit()
            session_state.flag_for_load = False
            rerun()
    with right:
        if button("No", type="primary", width="stretch"):
            rerun()


@dialog("Delete all tables", width="small", position="center")
def delete_all_tables(engine: Engine) -> None:
    """
    Confirm whether to delete all tables

    :param engine: The database engine
    :return: None
    """
    caption("Would you like to delete all tables?")

    left, right = columns(2)
    with left:
        if button("Yes", type="secondary", width="stretch"):
            DECLARATION.metadata.drop_all(engine)
            session_state.flag_for_load = False
            rerun()
    with right:
        if button("No", type="primary", width="stretch"):
            rerun()


@dialog("Delete the database", width="small", position="center")
def delete_db(engine: Engine, db_path: Path) -> None:
    """
    Confirm whether to delete the database

    :param engine: The database engine
    :param db_path: The database path
    :return: None
    """
    caption("Would you like to delete the database?")

    left, right = columns(2)
    with left:
        if button("Yes", type="secondary", width="stretch"):
            engine.dispose()

            if db_path.exists():
                remove(db_path)

            session_state.flag_for_load = False
            rerun()
    with right:
        if button("No", type="primary", width="stretch"):
            rerun()


@dialog("Delete selected data", width="small", position="center")
def delete_selected_data(engine: Engine, table: Any, db_idx: int) -> None:
    """
    Confirm whether to delete selected data

    :param engine: The database engine
    :param table: The table object
    :param db_idx: The database index
    :return: None
    """
    caption("Would you like to delete the selected data?")

    left, right = columns(2)
    with left:
        if button("Yes", type="secondary", width="stretch"):
            with InitSession(engine).init() as session:
                record = session.query(table).filter(table.id == db_idx).first()
                if record:
                    session.delete(record)
                    session.commit()
                rerun()
    with right:
        if button("No", type="primary", width="stretch"):
            rerun()


@dialog("Load default data", width="small", position="center")
def load_default_data(engine: Engine, table: Any) -> None:
    """
    Load default data into the database

    :param engine: The database engine
    :param table: The table object
    :return: None
    """
    caption("Would you like to load default data from the current Excel?")

    left, right = columns(2)
    with left:
        if button("Yes", type="secondary", width="stretch"):
            with TabularLoader(EXCEL, display=False) as loader:
                exercises: DataFrame = loader.load(file_category=TabularFormats.EXCEL)
                # print(exercises)
                with InitSession(engine).init() as session:
                    for _, row in exercises.iterrows():
                        new_record = table(
                            date=row.get("date"),
                            time=row.get("time"),
                            week=row.get("week"),
                            type=row.get("type"),
                            slope=row.get("slope"),
                            duration=row.get("duration"),
                            distance=row.get("distance"),
                            active_kilocalories=row.get("active_kilocalories"),
                            total_kilocalories=row.get("total_kilocalories"),
                            avg_cadence=row.get("avg_cadence"),
                            avg_pace=row.get("avg_pace"),
                            avg_heart_rate=row.get("avg_heart_rate"),
                            effort=row.get("effort"),
                            zone_i=row.get("zone_i"),
                            zone_ii=row.get("zone_ii"),
                            zone_iii=row.get("zone_iii"),
                            zone_iv=row.get("zone_iv"),
                            zone_v=row.get("zone_v"),
                            post_heart_rate_i=row.get("post_heart_rate_i"),
                            post_heart_rate_ii=row.get("post_heart_rate_ii"),
                            post_heart_rate_iii=row.get("post_heart_rate_iii"),
                            weight=row.get("weight"),
                            rpe=row.get("rpe"),
                        )
                        session.add(new_record)
                    session.commit()
            session_state.flag_for_load = True
            rerun()
    with right:
        if button("No", type="primary", width="stretch"):
            rerun()


def map_col_labels(data: str) -> str:
    """ Map column labels to a more readable format """
    abbreviations: dict[str, str] = {
        "ii": "II", "iii": "III", "iv": "IV",
        "rpe": "RPE",
    }
    return " ".join(abbreviations.get(word, word.capitalize()) for word in data.split("_"))


def transform_minutes_to_time(minutes: float) -> date_time:
    """
    Transform float minutes to time formate

    :param minutes: The minutes to transform
    :return: The transformed time
    """
    if not minutes:
        return date_time.min

    total: int = int(minutes * 60)
    hours: int = round(total // 3600, 2)
    minutes: int = round((total % 3600) // 60, 2)
    seconds: int = round(total % 60, 2)
    return date_time(hours, minutes, seconds)


def transform_time_to_minutes(t: date_time) -> float:
    """
    Transform time to minutes

    :param t: The time to transform
    :return: The transformed minutes
    """
    return round(t.hour * 60.0 + t.minute + t.second / 60.0, 2)


@dialog("Update the data", width="medium", position="center")
def update_data(engine: Engine, table: Any, db_idx: int) -> None:
    """
    Update an existing exercise record

    :param engine: The database engine
    :param table: The table object
    :param db_idx: The database index
    :return: None
    """
    notification = empty()

    with InitSession(engine).init() as session:
        record = session.query(table).filter(table.id == db_idx).first()
        print(record)

        if not record:
            notification.error("The record you are looking for does not exist.")
            return

        caption("Basic Information:")
        spades, hearts, diamonds, clubs = columns(4)
        with spades:
            date: date_date = date_input(
                "Exercise Date", value=record.date,
                width="stretch", help="Select the exercise date."
            )
        with hearts:
            time: date_time = time_input(
                "Exercise Time", value=record.time, step=timedelta(seconds=1),
                width="stretch", help="Select the exercise time."
            )
        with diamonds:
            weeks: list[str] = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            week_idx: int = weeks.index(record.week) if record.week in weeks else 0
            week: str = selectbox(
                "Exercise Week", options=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], index=week_idx,
                width="stretch", help="Select the exercise week."
            )
        with clubs:
            update_date: date_date = date_input(
                "Update Data Date", value=datetime.now(), disabled=True,
                width="stretch", help="Select the exercise date."
            )

        caption("Exercise Details:")
        desc, details = columns(2)
        with desc:
            category: str = segmented_control(
                "Exercise Category", options=["J", "R"], default=record.type, disabled=True,
                width="stretch", help="Select the exercise category."
            )
            slope: float = slider(
                "Exercise Slope", min_value=0.0, max_value=10.0, step=1.0, value=record.slope,
                width="stretch", help="Select the exercise slope."
            )
            duration: float = number_input(
                "Exercise Duration", min_value=0.0, max_value=100.0, step=0.01, value=record.duration,
                width="stretch", help="Select the exercise duration."
            )
            distance: float = number_input(
                "Exercise Distance", min_value=0.0, max_value=50.0, step=0.01, value=record.distance,
                width="stretch", help="Select the exercise distance."
            )
            active_kilocalories: float = number_input(
                "Exercise Active Calories", min_value=0.0, max_value=1000.0, step=1.0, value=record.active_calories,
                width="stretch", help="Select the exercise active calories."
            )
            total_kilocalories: float = number_input(
                "Exercise Total Calories", min_value=0.0, max_value=1000.0, step=1.0, value=record.total_calories,
                width="stretch", help="Select the exercise total calories."
            )
            avg_cadence: int = slider(
                "Exercise Average Cadence", min_value=0, max_value=200, step=1, value=record.avg_cadence,
                width="stretch", help="Select the exercise average cadence."
            )
            avg_pace: float = number_input(
                "Exercise Average Pace", min_value=0.0, max_value=50.0, step=0.01, value=record.avg_pace,
                width="stretch", help="Select the exercise average pace."
            )
            avg_heart_rate: int = slider(
                "Exercise Average Heart Rate", min_value=0, max_value=200, step=1, value=record.avg_heart_rate,
                width="stretch", help="Select the exercise average heart rate."
            )
            effort: int = slider(
                "Exercise Effort", min_value=0, max_value=10, step=1, value=record.effort,
                width="stretch", help="Select the exercise effort."
            )

        with details:
            zone_i: float = number_input(
                "Heart Rate Zone I", min_value=0.0, max_value=100.0, step=0.01, value=record.zone_i,
                width="stretch", help="Select the exercise zone I."
            )
            zone_ii: float = number_input(
                "Heart Rate Zone II", min_value=0.0, max_value=100.0, step=0.01, value=record.zone_ii,
                width="stretch", help="Select the exercise zone II."
            )
            zone_iii: float = number_input(
                "Heart Rate Zone III", min_value=0.0, max_value=100.0, step=0.01, value=record.zone_iii,
                width="stretch", help="Select the exercise zone III."
            )
            zone_iv: float = number_input(
                "Heart Rate Zone IV", min_value=0.0, max_value=100.0, step=0.01, value=record.zone_iv,
                width="stretch", help="Select the exercise zone IV."
            )
            zone_v: float = number_input(
                "Heart Rate Zone V", min_value=0.0, max_value=100.0, step=0.01, value=record.zone_v,
                width="stretch", help="Select the exercise zone V."
            )
            post_heart_rate_i: int = slider(
                "Post-Exercise Heart Rate I", min_value=0, max_value=200, step=1,
                value=record.post_heart_rate_i,
                width="stretch", help="Select the post-exercise heart rate Immediately."
            )
            post_heart_rate_ii: int = slider(
                "Post-Exercise Heart Rate II", min_value=0, max_value=200, step=1,
                value=record.post_heart_rate_ii,
                width="stretch", help="Select the post-exercise heart rate after 1 minute."
            )
            post_heart_rate_iii: int = slider(
                "Post-Exercise Heart Rate III", min_value=0, max_value=200, step=1,
                value=record.post_heart_rate_iii,
                width="stretch", help="Select the post-exercise heart rate after 2 minutes."
            )
            weight: float = number_input(
                "Exercise Weight", min_value=0.0, max_value=200.0, step=0.01, value=record.weight,
                width="stretch", help="Select the exercise weight."
            )
            rpe: int = slider(
                "Training Intensity (RPE)", min_value=0, max_value=10, step=1, value=record.rpe,
                width="stretch", help="Select the training intensity (RPE)."
            )

        if button("Submit", type="primary", width="stretch"):
            if record:
                record.date = date
                record.time = time
                record.week = week
                record.type = category
                record.slope = slope
                record.duration = duration
                record.distance = distance
                record.active_kilocalories = active_kilocalories
                record.total_kilocalories = total_kilocalories
                record.avg_cadence = avg_cadence
                record.avg_pace = avg_pace
                record.avg_heart_rate = avg_heart_rate
                record.effort = effort
                record.zone_i = zone_i
                record.zone_ii = zone_ii
                record.zone_iii = zone_iii
                record.zone_iv = zone_iv
                record.zone_v = zone_v
                record.post_heart_rate_i = post_heart_rate_i
                record.post_heart_rate_ii = post_heart_rate_ii
                record.post_heart_rate_iii = post_heart_rate_iii
                record.weight = weight
                record.rpe = rpe
                record.update_date = update_date

                session.commit()
            rerun()
