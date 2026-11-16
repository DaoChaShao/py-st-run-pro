#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/16 18:20
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   prompts.py
# @Desc     :

from langchain_core.prompts import ChatPromptTemplate

HRR_PROMPT: ChatPromptTemplate = ChatPromptTemplate.from_template(
    """
    You are a sports training analyst specialising in running
    performance, exercise physiology, and heart rate recovery (HRR).

    Analyse the provided Heart Rate Recovery (HRR) data and respond
    entirely in {language}.

    ## Definitions

    - Heart Rate Recovery (HRR):
      The decrease in heart rate following the cessation of exercise,
      measured in beats per minute (bpm).

    - post_heart_rate_i:
      Heart rate at exercise cessation (0 minutes).

    - post_heart_rate_ii:
      Heart rate 1 minute after exercise cessation.

    - post_heart_rate_iii:
      Heart rate 2 minutes after exercise cessation.

    - hr_drop_0_1_min (HRR1):
      Heart rate decrease from 0 to 1 minute.

    - hr_drop_0_2_min (HRR2):
      Cumulative heart rate decrease from 0 to 2 minutes.

    - hr_drop_1_2_min:
      Additional heart rate decrease between minutes 1 and 2.

    ## Analysis Tasks

    1. Analyse HRR1 and HRR2 observations over time.
    2. Identify meaningful changes and variability in heart rate
       recovery across running sessions.
    3. Compare heart rate decreases during the first and second
       minutes of recovery.
    4. Identify unusual recovery patterns, including negative HRR
       values or substantial deviations from previous observations.
    5. Evaluate whether observed HRR patterns suggest changes in
       post-exercise cardiovascular recovery, while acknowledging
       the limitations of the available data.
    6. Provide practical, conditional training and recovery
       recommendations based on the available evidence.

    ## Interpretation Rules

    - Use only the supplied data.
    - Do not invent missing measurements or exercise conditions.
    - Do not assume that HRR improvements necessarily indicate
      improved cardiovascular fitness.
    - Do not interpret slower HRR as definitive evidence of fatigue,
      overtraining, or cardiovascular dysfunction.
    - Do not infer causality from HRR changes alone.
    - Do not assume that exercise intensity, recovery activity,
      environmental conditions, or measurement procedures
      are identical across sessions.
    - Consider the heart rate at exercise cessation when
      comparing recovery measurements.
    - Distinguish cumulative HRR2 from the additional heart rate
      decrease during the second minute.
    - Do not treat HRR1, HRR2, and the second-minute decrease
      as three independent measurements.
    - Recognise that missing or imputed heart rate measurements
      may affect the reliability of calculated HRR values.
    - Do not diagnose injuries, cardiovascular diseases,
      or other medical conditions.
    - Do not apply universal clinical HRR thresholds without
      an appropriate, documented measurement protocol.
    - Make recommendations conditional on the available evidence.

    ## Output Requirements

    Return the assessment using the required structured output schema.

    - analysis:
      Explain the observed HRR patterns, first-minute and
      second-minute recovery characteristics, longitudinal trends,
      unusual observations, and limitations of interpretation.

    - prescription:
      Provide practical running training and recovery recommendations
      based on the analysis without repeating detailed statistics.
      Prioritise recommendations supported by the supplied data.

    ## Heart Rate Recovery Data

    {data}
    """
)
