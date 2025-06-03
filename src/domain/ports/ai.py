from abc import ABC, abstractmethod
from typing import Dict, List
from src.data.prompt import PROMPT


class AiConnector(ABC):
    """Interface abstraite (contrat) pour les connecteurs d'IA."""

    @abstractmethod
    def summarize_text(self, file_name: str, text: str) -> str:
        """
        Summarize content of PDF
        :param file_name: file name
        :param text: content of pdf
        :return: summarized text
        """
        pass

    @abstractmethod
    def response_with_context(self, question: str, context: str, history: List[Dict[str, str]]) -> str:
        """
        :param question: question
        :param context: context embedding
        :param history: history conversation
        :return: response of LLM
        """
        pass

    @abstractmethod
    def _check(self) -> Exception|None:
        """
        Check for use this connector
        :return: Exception or None
        """
        pass


# STATIC ---------------------------------------------------------------------------------------------------------------
    @staticmethod
    def clean_result(text: str) -> str:
        import re
        return re.sub(r'```', '', text)

    @staticmethod
    def get_prompt() -> str:
        return PROMPT