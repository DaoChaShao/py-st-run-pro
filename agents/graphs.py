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

from .acwr.nodes import acwr_node_assess, acwr_node_calculate
from .acwr.prompts import ACWR_PROMPT
from .acwr.states import ACWRContext, ACWRInput, ACWROutput, ACWRState
from .ef.nodes import ef_node_assess
from .ef.prompts import EF_PROMPT
from .ef.states import EFContext, EFInput, EFOutput
from .forks import AgentInitialiser
from .hrr.nodes import hrr_node_assess
from .hrr.prompts import HRR_PROMPT
from .hrr.states import HRRContext, HRRInput, HRROutput
from .types import ModelCategories, ModelOutputMethods


class ACWRGrapher(Access):
    """ Acute:Chronic Workload Ratio Assessment Grapher """

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
        self._prompt: ChatPromptTemplate = ACWR_PROMPT
        self._method: ModelOutputMethods = ModelOutputMethods.JSON_SCHEMA

    @staticmethod
    def _init_graph() -> Any:
        """ Initialise the graph """
        builder: StateGraph = StateGraph(ACWRState, ACWRContext, input_schema=ACWRInput, output_schema=ACWROutput)

        builder.add_node("calculator", acwr_node_calculate)
        builder.add_node("assessment", acwr_node_assess)

        builder.add_edge(START, "calculator")
        builder.add_edge("calculator", "assessment")
        builder.add_edge("assessment", END)
        return builder.compile()

    @protectedmethod
    def _init_agent(self) -> ACWRContext:
        """ Initialise the agent context """
        with AgentInitialiser(
                self._key,
                model=self._category.value, temperature=self._temperature,
        ) as agent:
            return ACWRContext(
                agent=agent.initialise(), prompt=self._prompt, method=self._method,
                language=self._language
            )

    def graph(self) -> tuple[Any, list[str]]:
        """ Graph the ACWR data """
        graph: Any = self._init_graph()
        agent: ACWRContext = self._init_agent()
        data: ACWRInput = ACWRInput(status="Start", data=self._data)
        return graph.invoke(data, context=agent), agent.logs

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


class EFGrapher(Access):
    """ Efficiency Factor Assessment Grapher """

    def __init__(
            self,
            ef: DataFrame,
            api_key: str,
            *,
            model: str | ModelCategories | ModelCategories | Literal["DeepSeek", "OpenAI"] = "DeepSeek",
            temperature: float = 0.0,
            language: str | Languages | Literal["English", "Chinese"] = "English",
    ) -> None:
        """
        Initialise the Efficiency Factor Assessment Grapher

        :param ef: The Efficiency Factor data to be graphed
        :param language: str | Languages | Literal["English", "Chinese"]
        :param model: str | ModelCategories | Literal["DeepSeek", "OpenAI"]
        :param temperature: float
        """
        super().__init__()
        self._data: DataFrame = ef
        self._key: str = api_key
        self._category: ModelCategories = ModelCategories(model)
        self._temperature: float = temperature
        self._language: Languages = Languages(language)
        self._prompt: ChatPromptTemplate = EF_PROMPT
        self._method: ModelOutputMethods = ModelOutputMethods.JSON_SCHEMA

    @staticmethod
    def _init_graph() -> Any:
        """ Initialise the graph """
        builder: StateGraph = StateGraph(EFInput, EFContext, input_schema=EFInput, output_schema=EFOutput)

        builder.add_node("assessment", ef_node_assess)

        builder.add_edge(START, "assessment")
        builder.add_edge("assessment", END)
        return builder.compile()

    @protectedmethod
    def _init_agent(self) -> EFContext:
        """ Initialise the Agent Context """
        with AgentInitialiser(
                self._key,
                model=self._category.value, temperature=self._temperature,
        ) as agent:
            return EFContext(
                agent=agent.initialise(), prompt=self._prompt, method=self._method,
                language=self._language
            )

    def graph(self) -> tuple[Any, list[str]]:
        """ Graph the Efficiency Factor data """
        graph: Any = self._init_graph()
        agent: EFContext = self._init_agent()
        data: EFInput = EFInput(status="Start", data=self._data)
        return graph.invoke(data, context=agent), agent.logs

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


class HRRGrapher(Access):
    """ Heart Rate Recovery Assessment Grapher """

    def __init__(
            self,
            hrr: DataFrame,
            api_key: str,
            *,
            model: str | ModelCategories | ModelCategories | Literal["DeepSeek", "OpenAI"] = "DeepSeek",
            temperature: float = 0.0,
            language: str | Languages | Literal["English", "Chinese"] = "English",
    ) -> None:
        """
        Initialise the Heart Rate Recovery Assessment Grapher

        :param hrr: The Heart Rate Recovery data to be graphed
        :param hrr: DataFrame
        :param language: str | Languages | Literal["English", "Chinese"]
        :param model: str | ModelCategories | Literal["DeepSeek", "OpenAI"]
        :param temperature: float
        """
        super().__init__()
        self._data: DataFrame = hrr
        self._key: str = api_key
        self._category: ModelCategories = ModelCategories(model)
        self._temperature: float = temperature
        self._language: Languages = Languages(language)
        self._prompt: ChatPromptTemplate = HRR_PROMPT
        self._method: ModelOutputMethods = ModelOutputMethods.JSON_SCHEMA

    @staticmethod
    def _init_graph() -> Any:
        """ Initialise the graph """
        builder: StateGraph = StateGraph(HRRInput, HRRContext, input_schema=HRRInput, output_schema=HRROutput)

        builder.add_node("assessment", hrr_node_assess)

        builder.add_edge(START, "assessment")
        builder.add_edge("assessment", END)
        return builder.compile()

    @protectedmethod
    def _init_agent(self) -> HRRContext:
        """ Initialise the Agent Context """
        with AgentInitialiser(
                self._key,
                model=self._category.value, temperature=self._temperature,
        ) as agent:
            return HRRContext(
                agent=agent.initialise(), prompt=self._prompt, method=self._method,
                language=self._language
            )

    def graph(self) -> tuple[Any, list[str]]:
        """ Graph the Efficiency Factor data """
        graph: Any = self._init_graph()
        agent: HRRContext = self._init_agent()
        data: HRRInput = HRRInput(status="Start", data=self._data)
        return graph.invoke(data, context=agent), agent.logs

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
