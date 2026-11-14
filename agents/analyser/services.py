#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/12 22:33
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   services.py
# @Desc     :

from typing import Self

from langchain_core.prompts import ChatPromptTemplate
from pandas import DataFrame

from utils.helper import Access

PROMPT: ChatPromptTemplate = ChatPromptTemplate.from_template(
    """
    You are a professional sports training analyst specialising in
    exercise physiology, training load monitoring, and performance analysis.

    Analyse the provided training workload statistics and respond
    entirely in {language}.

    #### Metric Definitions

    - Objective workload:
      Apple Watch effort × exercise duration.

    - Subjective workload:
      User-reported RPE × exercise duration.

    - Acute workload:
      Cumulative training workload over the previous 7 calendar days.

    - Chronic workload:
      Cumulative training workload over the previous 28 calendar days,
      divided by 4 to obtain the average weekly workload.

    - ACWR:
      Acute workload divided by chronic workload.

    - Difference:
      Objective ACWR minus subjective ACWR.

    #### Statistical Definitions

    Each available metric may contain:

    - latest: Most recent available observation.
    - mean: Arithmetic mean of available observations.
    - min: Minimum observed value.
    - max: Maximum observed value.
    - trend: Difference between the last and first available observations.

    IMPORTANT:
    - "trend" represents endpoint change, NOT a regression slope.
    - Do not interpret endpoint change as a statistically significant trend.
    - Do not claim a continuous increase or decrease without supporting data.
    - Do not infer the duration or rate of change from endpoint differences.
    - Do not infer statistical significance, correlation, or causality
      from summary statistics alone.

    #### Analysis Tasks

    1. Objective Workload Analysis
       - Evaluate session workload, acute workload, chronic workload,
         and ACWR when available.
       - Describe the latest values relative to their historical
         means and observed ranges.
       - Identify notable changes without overstating their significance.

    2. Subjective Workload Analysis
       - Apply the same analytical approach to subjective workload.
       - Evaluate changes in perceived training load without assuming
         that higher subjective values necessarily indicate fatigue.

    3. Objective–Subjective Comparison
       - Compare objective and subjective workload patterns.
       - Compare objective and subjective ACWR values when available.
       - Interpret the direction and magnitude of ACWR differences.
       - Identify discrepancies that may warrant further monitoring.

       IMPORTANT:
       - Apple Watch effort and user RPE are different measurement systems.
       - Their absolute workload values are not necessarily directly
         comparable without calibration.
       - A higher subjective workload does not automatically indicate
         accumulated fatigue.
       - ACWR differences do not establish that either measurement
         system is inaccurate.
       - Do not infer device underestimation or user overestimation
         from numerical differences alone.

    4. Overall Training Assessment
       - Summarise the most relevant workload observations.
       - Distinguish observed facts from possible explanations.
       - Explain uncertainty and limitations where appropriate.

    #### Training Prescription

    Provide practical, evidence-informed, and conditional recommendations
    based exclusively on the available statistics.

    Consider:
    - Training load progression or reduction.
    - Training intensity and volume management.
    - Recovery and adaptation.
    - Objective–subjective workload discrepancies.
    - Continued monitoring and reassessment.

    IMPORTANT:
    - Do not prescribe fixed percentage increases in training workload
      without sufficient individual evidence.
    - Do not treat specific ACWR thresholds as universally safe or unsafe.
    - Do not diagnose fatigue, overtraining, injuries, or medical conditions.
    - Do not assume the athlete's goals, training phase, or recovery status.
    - Where information is insufficient, provide conditional alternatives
      rather than unsupported definitive recommendations.

    #### Output Requirements

    Return the assessment using the required structured output schema.

    The schema contains two fields:

    1. analysis
       - Provide a structured interpretation of the available statistics.
       - Organise the discussion into clear sections.
       - Explain objective workload, subjective workload,
         ACWR comparison, and key findings.
       - Focus on observations and interpretation.
       - Do NOT include training prescriptions or action plans.

    2. prescription
       - Provide actionable training and recovery recommendations.
       - Base recommendations on the findings in "analysis".
       - Explain the rationale for each recommendation.
       - Use conditional language when evidence is limited.
       - Avoid repeating detailed statistical descriptions
         already presented in "analysis".

    #### General Rules

    - Use only the supplied data.
    - Do not invent missing measurements or training history.
    - Do not interpret unavailable metrics.
    - Do not assume that missing ACWR values indicate zero workload.
    - Treat ACWR as a descriptive workload indicator, not a
      validated standalone injury-risk prediction tool.
    - Distinguish numerical observations from hypotheses.
    - Avoid unsupported causal claims.
    - Use consistent terminology and units.
    - Use clear, professional language appropriate for sports science.
    - Format each output field using valid Markdown.
    - Use headings and bullet points where appropriate.
    - Avoid redundant content between analysis and prescription.

    #### Training Statistics

    {statistics}
    """
)


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
