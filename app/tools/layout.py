#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/7 15:10
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   layout.py
# @Desc     :

from streamlit import Page, navigation, set_page_config


def config_page() -> None:
    """ Set the window
    :return: None
    """
    set_page_config(
        page_title="Runner Pro Analyst",
        page_icon=":material/globe:",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def set_pages() -> None:
    """ Set the subpages on the sidebar (https://fonts.google.com/icons)
    :return: None
    """
    pages: dict = {
        "page": [
            "app/subpages/home.py",
            "app/subpages/preparation.py",
            # "app/subpages/monitor.py",
            # "app/subpages/prescription.py"
        ],
        "title": [
            "Home",
            "Database Preparation",
            # "Load & Fatigue Monitoring",
            # "AI-Driven Training Load Prescription"
        ],
        "icon": [
            ":material/home:",
            ":material/dashboard:",
            # ":material/dashboard_2_gear:",
            # ":material/browse_activity:",
            # ":material/clinical_notes:"
        ],
    }

    structure: dict = {
        "Introduction": [
            Page(page=pages["page"][0], title=pages["title"][0], icon=pages["icon"][0]),
        ],
        "Core Functions": [
            Page(page=pages["page"][1], title=pages["title"][1], icon=pages["icon"][1]),
            # Page(page=pages["page"][2], title=pages["title"][2], icon=pages["icon"][2]),
            # Page(page=pages["page"][3], title=pages["title"][3], icon=pages["icon"][3]),
            # Page(page=pages["page"][4], title=pages["title"][4], icon=pages["icon"][4]),
        ],
    }
    pg = navigation(structure, position="sidebar", expanded=True)
    pg.run()
