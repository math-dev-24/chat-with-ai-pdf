import os
from typing import Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

from domain.ports.ai import AiConnector


class OpenAiConnector(AiConnector):
    def initialize(self, config: Dict[str, Any]) -> None:
        load_dotenv()

    def summarize_text(self, file_name: str, text: str) -> str:
        print(f"✍️ Génération du résumé : {file_name}")

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages, # type: ignore
            temperature=0.3,
            max_tokens=4000
        )

        return AiConnector.clean_result(response.choices[0].message.content)