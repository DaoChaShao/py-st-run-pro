#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/11/13 16:08
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   graphs.py
# @Desc     :

from typing import Any, Literal, Self

from access_modifiers import protectedmethod
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START, StateGraph
from pandas import DataFrame

from utils.helper import Access
from utils.types import Languages

from ..forks import AgentInitialiser
from ..types import ModelCategories, ModelOutputMethods
from .nodes import node_assess, node_calculate
from .services import PROMPT
from .states import Context, Input, Output, State


class ACWRGrapher(Access):
    """ Acute:Chronic Workload Assessment Grapher """

    def __init__(
            self,
            acwr: DataFrame,
            api_key: str,
            *,
            model: str | ModelCategories | ModelCategories | Literal["DeepSeek", "OpenAI"] = "DeepSeek",
            temperature: float = 0.0,
            language: str | Languages | Literal["English", "Chinese"] = "English",
    ) -> None:
        """
        Initialise the ACWR Grapher

        :param acwr: The ACWR data to be graphed
        :type acwr: DataFrame
        :type language: str | Languages | Literal["English", "Chinese"]
        :type model: str | ModelCategories | Literal["DeepSeek", "OpenAI"]
        :type temperature: float
        """
        super().__init__()
        self._data: DataFrame = acwr
        self._key: str = api_key
        self._category: ModelCategories = ModelCategories(model)
        self._temperature: float = temperature
        self._language: Languages = Languages(language)
        self._prompt: ChatPromptTemplate = PROMPT
        self._method: ModelOutputMethods = ModelOutputMethods.JSON_SCHEMA

    @staticmethod
    def _init_graph() -> Any:
        """ Initialise the graph """
        builder: StateGraph = StateGraph(State, Context, input_schema=Input, output_schema=Output)

        builder.add_node("calculator", node_calculate)
        builder.add_node("assessment", node_assess)

        builder.add_edge(START, "calculator")
        builder.add_edge("calculator", "assessment")
        builder.add_edge("assessment", END)
        return builder.compile()

    @protectedmethod
    def _init_agent(self) -> Context:
        """ Initialise the agent """
        with AgentInitialiser(
                self._key,
                model=self._category.value, temperature=self._temperature,
        ) as agent:
            return Context(agent=agent.initialise(), prompt=self._prompt, method=self._method, language=self._language)

    def graph(self) -> Any:
        """ Graph the ACWR data """
        graph: Any = self._init_graph()
        agent: Context = self._init_agent()
        data: Input = Input(status="Start", data=self._data)
        return graph.invoke(data, context=agent)

    def __enter__(self) -> Self:
        """ Contextual management """
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Contextual management

        :param exc_type: The type of exception that occurred.
        :param exc_value: The exception that occurred.
        :param traceback: The traceback of the exception.
        :return: Whether the exception was handled.
        """
        pass
