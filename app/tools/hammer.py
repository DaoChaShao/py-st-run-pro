#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/7 16:31
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   hammer.py
# @Desc     :

from datetime import date as date_date
from datetime import time as date_time
from typing import Any

from sqlalchemy.engine import Engine
from streamlit import (
    balloons,
    button,
    caption,
    columns,
    date_input,
    dialog,
    number_input,
    rerun,
    segmented_control,
    selectbox,
    slider,
    time_input,
)

from utils.dbk import InitSession


@dialog("Cast your exercise", width="medium", position="center")
def new_exercise(engine: Engine, table: Any):
    caption("Basic Information:")
    left, mid, right = columns(3)
    with left:
        date: date_date = date_input(
            "Exercise Date", value=date_date.today(),
            width="stretch", help="Select the exercise date."
        )
    with mid:
        time: date_time = time_input(
            "Exercise Time", value=date_time.min,
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
        slope: int = slider(
            "Exercise Slope", min_value=0, max_value=10, value=3, step=1,
            width="stretch", help="Select the exercise slope."
        )
        duration: date_time = time_input(
            "Exercise Duration", value=date_time.min,
            width="stretch", help="Select the exercise duration."
        )
        distance: float = number_input(
            "Exercise Distance", min_value=0.0, max_value=50.0, value=5.00, step=0.01,
            width="stretch", help="Select the exercise distance."
        )
        active_calories: int = number_input(
            "Exercise Active Calories", min_value=0, max_value=1000, step=1,
            width="stretch", help="Select the exercise active calories."
        )
        total_calories: int = number_input(
            "Exercise Total Calories", min_value=0, max_value=1000, step=1,
            width="stretch", help="Select the exercise total calories."
        )
        avg_cadence: int = slider(
            "Exercise Average Cadence", min_value=0, max_value=200, step=1,
            width="stretch", help="Select the exercise average cadence."
        )
        avg_pace: date_time = time_input(
            "Exercise Average Pace", value=date_time.min,
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
        zone_i: date_time = time_input(
            "Heart Rate Zone I", value=date_time.min,
            width="stretch", help="Select the exercise zone I."
        )
        zone_ii: date_time = time_input(
            "Heart Rate Zone II", value=date_time.min,
            width="stretch", help="Select the exercise zone II."
        )
        zone_iii: date_time = time_input(
            "Heart Rate Zone III", value=date_time.min,
            width="stretch", help="Select the exercise zone III."
        )
        zone_iv: date_time = time_input(
            "Heart Rate Zone IV", value=date_time.min,
            width="stretch", help="Select the exercise zone IV."
        )
        zone_v: date_time = time_input(
            "Heart Rate Zone V", value=date_time.min,
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

    if button("Submit"):
        with InitSession(engine).init() as session:
            exercise = table(
                date=date,
                time=time,
                week=week,
                type=category,

                slope=slope,
                duration=duration,
                distance=distance,
                active_calories=active_calories,
                total_calories=total_calories,
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

        balloons()
        rerun()
