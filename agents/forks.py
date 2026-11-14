#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/12 21:59
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   forks.py
# @Desc     :

from pathlib import Path
from typing import Literal, Self

from access_modifiers import protectedmethod
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from yaml import dump, safe_load

from agents.types import (
    ModelCategories,
)
from utils.helper import Access


class AgentInitialiser(Access):
    """ Agent Initialiser """

    def __init__(
            self,
            api_key: str | SecretStr,
            *,
            model: str | ModelCategories | Literal["DeepSeek", "OpenAI"] = "DeepSeek",
            temperature: float = 0.0,
    ) -> None:
        """
        Initialise the Agent Initialiser

        :param api_key: API key for authentication
        :param model: Model category (deepseek or openai)
        :param temperature: Temperature parameter for the language model
        :return: None
        """
        super().__init__()
        self._key: SecretStr = SecretStr(api_key)
        self._category: ModelCategories = ModelCategories(model)
        self._temperature: float = temperature
        self._llm = None

    @protectedmethod
    def _init_seeker(
            self,
            *,
            model: str | Literal["deepseek-v4-flash", "deepseek-v4-pro"] = "deepseek-v4-flash",
            url: str | Literal[
                "https://api.deepseek.com",
                "https://api.deepseek.com/anthropic"
            ] = "https://api.deepseek.com",
            thinking_mode: str | Literal["enabled", "disabled"] = "disabled"
    ) -> ChatDeepSeek:
        """
        Initialise the DeepSeek model

        :param model: Model name
        :param url: Base URL
        :param thinking_mode: Thinking mode
        :return: Model instance
        """
        return ChatDeepSeek(
            api_key=self._key,
            model=model,
            base_url=url,
            temperature=self._temperature,
            extra_body={"thinking": {"type": thinking_mode}}
        )

    @protectedmethod
    def _init_opener(
            self,
            *,
            model: str | Literal["gpt-5.5-2026-04-23", "gpt-5.6-terra", "gpt-6-sol"] = "gpt-5.5-2026-04-23",
            url: str | Literal["https://api.openai.com/v1",] = "https://api.openai.com/v1",
    ) -> ChatOpenAI:
        """
        Initialise the OpenAI model

        :param model: Model name
        :param url: Base URL
        :return: Model instance
        """
        return ChatOpenAI(
            api_key=self._key,
            model=model,
            base_url=url,
            temperature=self._temperature
        )

    def initialise(self) -> ChatDeepSeek | ChatOpenAI:
        """ Initialise the LLM """
        match self._category:
            case ModelCategories.DEEPSEEK:
                return self._init_seeker()
            case ModelCategories.OPENAI:
                return self._init_opener()
            case _:
                raise ValueError(f"Invalid model category: {self._category}")

    def __enter__(self) -> Self:
        """ Enter the context manager. """
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        This method is called when the context manager is exited.

        :param exc_type: The type of the exception that was raised.
        :param exc_value: The exception instance that was raised.
        :param traceback: The traceback object associated with the exception.
        :return: `True` if the exception is handled, otherwise `False`.
        """
        self._llm = None


def load_yaml(filepath: str | Path, *, display: bool = True) -> dict:
    """
    Load and parse a YAML configuration file safely

    :param filepath: Path to the YAML file
    :param display: Whether to display the loading result
    :return: Dictionary containing YAML data
    """
    _path = Path(filepath)

    if not _path.exists():
        raise FileNotFoundError(f"YAML config file not found at: {_path}")

    with open(_path, encoding="utf-8") as file:
        data = safe_load(file)

    if display:
        print(f"Loaded YAML config from: {_path.resolve()}")
        print(dump(data, allow_unicode=True, sort_keys=False).strip())
    return data


def reducer(curr_state: str, new_state: str) -> str:
    """
    Reduce the logs list

    :param curr_state: Current state
    :param new_state: New state
    :return: Reduced state
    """
    if not curr_state:
        return new_state
    return curr_state + " -> " + new_state
