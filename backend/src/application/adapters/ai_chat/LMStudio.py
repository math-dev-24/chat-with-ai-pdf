import os
import requests
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from src.domain.ports.ai import AiConnector


class LmStudioAdapter(AiConnector):
    def __init__(self, **kwargs):
        load_dotenv()
        self.model: Optional[str] = os.getenv('LM_MODEL')
        self.base_url: Optional[str] = os.getenv('LM_STUDIO_URL')
        self.api_key: Optional[str] = os.getenv('LM_STUDIO_API_KEY')

        self.timeout: int = kwargs.get('timeout', 120)
        self.temperature: float = kwargs.get('temperature', 0.7)
        self.max_tokens: int = kwargs.get('max_tokens', 1000)

        self._check()
        self._health_check()


    def summarize_text(self, file_name: str, text: str) -> str:
        try:
            logging.info(f"Envoi de la request {file_name}")

            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=self._build_payload(text),
                headers=self._get_headers(),
                timeout=self.timeout
            )

            response.raise_for_status()

            response_data = response.json()

            if 'choices' in response_data and len(response_data['choices']) > 0:
                summary = response_data['choices'][0]['message']['content']
                return self.clean_result(summary)

            else:
                raise Exception("Réponse invalide de l'API LM Studio")

        except requests.exceptions.HTTPError as e:
            raise Exception(f"Erreur de communication avec LM Studio: {str(e)}")


    def response_with_context(self, question: str, context: str, historic: str) -> str:
        logging.info(f"Pas implémenter LM Studio response context")
        return ""


    def _check(self) -> None:
        if self.model is None:
            raise Exception('Model non défini !')

        if self.base_url is None:
            raise Exception('Base URL non défini !')

        if self.api_key is None:
            raise Exception("API KEY Non défini !")

        logging.info(f"Initialisation de LM Studio OK")


    def _health_check(self) -> bool:
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self._get_headers(),
                timeout=10
            )

            response.raise_for_status()

            models_data = response.json()
            available_models = [model.get('id', '') for model in models_data.get('data', [])]

            if self.model not in available_models:
                logging.warning(f"Modèle {self.model} non trouvé. Modèles disponibles: {available_models}")
                return False
            return True

        except Exception as e:
            logging.error(f"Health check échoué: {str(e)}")
            return False


    def _get_headers(self) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }


    def _build_payload(self, prompt: str) -> Dict[str, Any]:
        return {
            'model': self.model,
            'messages': [
                {
                    'role': 'system',
                    'content': AiConnector.get_prompt()
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'stream': False
        }