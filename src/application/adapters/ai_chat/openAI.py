import os, logging
from typing import List, Dict

from dotenv import load_dotenv
from openai import OpenAI
from src.domain.ports.ai import AiConnector


class OpenAiConnector(AiConnector):
    def __init__(self):
        load_dotenv()

        self.model: str|None = None
        self.api_key: str|None = None
        self.client: OpenAI|None = None

        self.model = os.getenv("OPENAI_MODEL", "gpt-4-1106-preview")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self._check()
        self._init_client()

    def summarize_text(self, file_name: str, text: str) -> str:
        print(f"✍️ Génération du résumé : {file_name}")

        chunks = [text[i:i + 8000] for i in range(0, len(text), 8000)]

        messages = [
            {
                "role": "system",
                "content": AiConnector.get_prompt()
            }
        ]

        for chunk in chunks[:2]:
            messages.append(
                {
                    "role": "user",
                    "content": f"Résume ce document :\n{chunk}"
                }
            )

        response = self.client.chat.completions.create(
            model= self.model,
            messages=messages, # type: ignore
            temperature=0.3,
            max_tokens=4000
        )

        return AiConnector.clean_result(response.choices[0].message.content)


    def response_with_context(self, question: str, context: str, historic: List[Dict[str, str]] = None) -> str:

        if historic is None:
            historic = []

        response = self.client.chat.completions.create(
            model= self.model,
            messages=self._generate_message(question, context, historic), # type: ignore
            temperature=0.3,
            max_tokens=4000
        )

        return AiConnector.clean_result(response.choices[0].message.content)


    def _check(self) -> None:
        if self.model is None:
            logging.error("OpenAI model non trouvé !")
            raise Exception('model not initialized')
        if self.api_key is None:
            logging.error("OpenAI API key non trouvé !")
            raise Exception('api_key not initialized')


    def _init_client(self) -> None:
        try:
            self.client = OpenAI(api_key=self.api_key)
        except Exception as e:
            logging.error(e)


    @staticmethod
    def _generate_message(question: str, context: str, historic: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
         Génère la liste des messages pour l'API OpenAI

         Args:
             question: Question actuelle
             context: Contexte technique
             historic: Historique des messages

         Returns:
             Liste des messages formatés pour OpenAI
         """

        system_message = {
            "role": "system",
            "content": """Tu es un assistant expert en technologie du froid industriel spécialisé dans les bouteilles séparatrices, 
            les systèmes de réfrigération et les équipements associés.

            Instructions :
            - Tu dois répondre au format HTML avec des balises appropriées (<p>, <h3>, <ul>, <li>, etc.)
            - Utilise l'historique de conversation pour maintenir la cohérence
            - Sois précis et technique tout en restant accessible
            - Si la question fait référence à des éléments précédents, utilise l'historique pour comprendre le contexte
            - Structure tes réponses de manière claire et logique"""
        }

        if not historic or len(historic) == 0:
            return [
                system_message,
                {
                    "role": "user",
                    "content": question
                },
                {
                    "role": "system",
                    "content": f"Contexte technique disponible :\n\n{context}"
                }
            ]

        messages = [system_message]

        limited_historic = historic[-8:] if len(historic) > 18 else historic

        for msg in limited_historic:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        messages.append({
            "role": "user",
            "content": question
        })

        messages.append({
            "role": "system",
            "content": f"Contexte technique pertinent pour cette question :\n\n{context}"
        })

        return messages