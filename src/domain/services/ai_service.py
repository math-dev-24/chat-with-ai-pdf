from typing import List, Dict

from src.domain.ports.ai import AiConnector


class AiService:
    def __init__(self, connector: AiConnector):
        self.connector = connector

    def summarize(self, file_name: str, text: str) -> str:
        return self.connector.summarize_text(file_name, text)

    def response(self, question: str, context: str, history: List[Dict[str, str]]) -> str:
        return self.connector.response_with_context(question, context, history)