from abc import ABC, abstractmethod
from typing import Dict, List


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
        text = re.sub(r'```html', '', text)
        text = re.sub(r'```', '', text)
        return text

    @staticmethod
    def get_prompt() -> str:
        with open("prompt.txt") as f:
            return f.read()