#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/7 15:11
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   home.py
# @Desc     :

from streamlit import caption, empty, expander, title

empty_message = empty()
empty_message.info("Please check the details at the different pages of core functions.")

title("Runner Pro")
with expander("**INTRODUCTION (CN)**", expanded=False):
    caption("- **数据管理（Data Management）**：读取和管理运动记录，为后续数据分析提供基础。")
    caption("- **数据质量与插补（Data Quality & Imputation）**：检查缺失值和重复记录，并支持多种缺失值插补方法。")
    caption("- **运动效率因子（EF）**：结合运动速度与平均心率，分析跑步效率及其变化趋势。")
    caption("- **急性与慢性训练负荷比（ACWR）**：分析短期与长期训练负荷之间的关系，辅助观察训练负荷变化。")
    caption("- **心率恢复（HRR）**：计算运动结束后第 1 分钟、第 2 分钟的心率下降指标，分析运动后心率恢复情况。")
    caption("- **交互式数据可视化（Data Visualisation）**：通过数据表格和图表展示运动指标及其时间变化趋势。")
    caption("- **人工智能辅助评估（AI Assessment）**：利用大语言模型分析运动数据，生成训练表现解读和条件性训练建议。")
    caption("- **可配置分析（Configurable Analysis）**：根据可用设置调整数据处理方法、AI 模型和分析语言。")
    caption("**注意：** 本应用提供的数据分析及 AI 建议仅供运动训练参考，不构成医学诊断或专业医疗建议。")


with expander("**INTRODUCTION (EN)**", expanded=True):
    caption("- **Data Management:** Load and manage exercise records for subsequent analysis.")
    caption("- **Data Quality & Imputation:** Check for missing values and duplicate records, and support multiple missing value imputation methods.")
    caption("- **Exercise Efficiency Factor (EF):** Combine exercise speed and average heart rate to analyze running efficiency and its trend changes.")
    caption("- **Acute to Chronic Workload Ratio (ACWR):** Analyze the relationship between short-term and long-term workload to assist in observing workload changes.")
    caption("- **Heart Rate Recovery (HRR):** Calculate heart rate decline indicators in the first and second minutes after exercise to analyze heart rate recovery.")
    caption("- **Interactive Data Visualization:** Display exercise metrics and their time trend changes through data tables and charts.")
    caption("- **AI Assessment:** Utilize large language models to analyze exercise data and generate training performance interpretations and conditional training recommendations.")
    caption("- **Configurable Analysis:** Adjust data processing methods, AI models, and analysis languages according to available settings.")
    caption("**Disclaimer:** The data analysis and AI suggestions provided by this application are for reference in exercise training and do not constitute medical diagnoses or professional medical advice.")
