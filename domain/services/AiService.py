from domain.ports.ai import AiConnector


class AiService:
    def __init__(self, connector: AiConnector):
        self.connector = connector


    def summarize(self, file_name: str, text: str) -> str:
        return self.connector.summarize_text(file_name, text)
