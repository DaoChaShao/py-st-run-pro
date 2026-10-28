#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/10/21 19:42
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   preprocessor.py
# @Desc     :

from pathlib import Path
from typing import Literal, Self

from access_modifiers import protectedmethod
from pandas import DataFrame, Series, read_csv, read_excel

from ..decorator import timer
from ..helper import Access
from ..highlighter import lines
from .types import TabularFormats


@timer
def get_cls_label_distribution(
        labels: Series,
        *,
        threshold: float = 1.5,
        display: bool = False
) -> tuple[Series, Series, float, bool, int]:
    """
    Check the distribution of the labels in the target variable and evaluate class balance.

    :param labels: The target label series.
    :param threshold: The Imbalance Ratio (IR) threshold to judge imbalance (default: 1.5).
    :param display: Whether to display formatted label counts, proportions, and balance verdict.
    :return: Tuple of (counts, proportions, imbalance_ratio, is_balanced)
    """
    _counts: Series = labels.value_counts()
    _proportions: Series = labels.value_counts(normalize=True)

    # Calculate Imbalance Rate (Max Count / Min Count)
    _max_count = int(_counts.max())
    _min_count = int(_counts.min()) if _counts.min() > 0 else 1
    ir: float = round(_max_count / _min_count, 2)

    # Determine if the class balance is acceptable
    _is_balanced: bool = ir < threshold

    # Determine the number of classes
    _n_classes: int = _counts.size

    # Display the label counts, proportions, and balance verdict
    if display:
        print(_counts)
        lines()
        print(_proportions)
        lines()
        print(f"Max Count / Min Count : {_max_count} / {_min_count}")
        print(f"Imbalance Ratio (IR)  : {ir:.2f}")

        # Provide an intuitive conclusion
        if ir < 1.5:
            verdict = "Balanced (Sample distribution is very balanced)"
        elif 1.5 <= ir < 3.0:
            verdict = "Mildly Imbalanced (Mild imbalance)"
        elif 3.0 <= ir < 5.0:
            verdict = "Moderately Imbalanced (Moderate imbalance, pay attention)"
        else:
            verdict = "Severely Imbalanced (Severe imbalance, resampling or weight setting required)"
        print(f"Status                : {verdict}")
        lines()
        print(f"Number of classes     : {_n_classes}")
    return _counts, _proportions, ir, _is_balanced, _n_classes


@timer
def get_reg_label_distribution(labels: Series, *, display: bool = True) -> dict:
    """
    Analyse the distribution features of continuous regression targets

    :param labels: the target variable
    :param display: Toggle for printing the distribution summary
    :return: the distribution summary
    """
    _stats: dict[str, float] = {
        "count": len(labels),
        "mean": labels.mean(),
        "std": labels.std(),
        "min": labels.min(),
        "25%": labels.quantile(0.25),
        "median": labels.median(),
        "75%": labels.quantile(0.75),
        "max": labels.max(),
        "skewness": labels.skew(),
        "kurtosis": labels.kurt(),
    }

    if display:
        for key, value in _stats.items():
            print(f"{key:<10}: {value:.4f}")
        lines()

        # Bias Situations
        if _stats["skewness"] > 1.0:
            print("Status: Highly Right-Skewed (Strongly recommend log1p transformation)")
        elif 0.5 < _stats["skewness"] <= 1.0:
            print("Status: Moderately Right-Skewed (Consider log1p transformation)")
        elif -1.0 <= _stats["skewness"] < -0.5:
            print("Status: Moderately Left-Skewed")
        elif _stats["skewness"] < -1.0:
            print("Status: Highly Left-Skewed")
        else:
            print("Status: Fairly Symmetric Distribution")
    return _stats


class TabularLoader(Access):
    """ Load and display data from a file. """

    def __init__(self, filepath: str | Path, *, display: bool = True) -> None:
        """
        Initialise the FileLoader class

        :param filepath: The path to the file.
        :param display: Whether to display the dataset content and summary.
        :return: None
        """
        super().__init__()
        self._path: Path = Path(filepath)
        self._type: TabularFormats | None = None
        self._display: bool = display
        self._dataset: DataFrame | None = None

    def load(self, file_category: str | TabularFormats | Literal["csv", "excel"] = TabularFormats.CSV) -> DataFrame:
        """
        Load data from a file based on the specified file category.

        :param file_category: The category of the file (csv or excel).
        :return: The loaded dataset.
        """
        self._type: TabularFormats = TabularFormats(file_category)
        match self._type:
            case TabularFormats.CSV:
                self._dataset = read_csv(self._path.resolve())
            case TabularFormats.EXCEL:
                self._dataset = read_excel(self._path.resolve())
            case _:
                raise ValueError(f"Invalid file category: {self._type}")

        if self._display:
            self._display_info()
        return self._dataset

    def __enter__(self) -> Self:
        """ Enter the context manager. """
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exit the context manager.

        :param exc_type: The type of exception that occurred.
        :param exc_value: The exception that occurred.
        :param traceback: The traceback of the exception.
        :return: None
        """
        pass

    @protectedmethod
    def _display_info(self) -> None:
        """ Display information: head, description, duplicated rows, missing values and missing values details. """
        if self._dataset is None:
            return

        print(self._dataset.head())
        print()
        print(self._dataset.describe())
        print()
        _dup_rows: float = self._dataset.duplicated().sum()
        _miss_values: float = self._dataset.isnull().sum().sum()
        _miss_details: Series = self._dataset.isnull().sum()[self._dataset.isnull().sum() > 0]
        print(f"Duplicated Rows: {_dup_rows}")
        print(f"Missing Values: {_miss_values}")
        if not _miss_details.empty:
            print(f"Missing Values Details:\n{_miss_details}")
        else:
            print("Missing Values Details: None")

    @property
    def dataset(self) -> DataFrame | None:
        """ Return the dataset """
        return self._dataset

    def __len__(self) -> int:
        """ Return the length of the dataset. """
        return len(self._dataset) if self._dataset is not None else 0

    def __repr__(self) -> str:
        """ Return the string representation of the FileLoader class. """
        return (
            f"TabularLoader("
            f"filepath={self._path!r}, "
            f"file_category={self._type!r}, "
            f"display={self._display!r})"
        )
