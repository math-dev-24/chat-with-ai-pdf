from abc import ABC, abstractmethod
from typing import Dict, Any

from data.prompt import PROMPT


class AiConnector(ABC):
    """Interface abstraite (contrat) pour les connecteurs d'IA."""

    @abstractmethod
    def summarize_text(self, file_name: str, text: str) -> str:
        """
        Résume un texte donné.

        Args:
            file_name: Nom du fichier ou identifiant du document
            text: Texte à résumer

        Returns:
            Résumé du texte
        """
        pass

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialise le connecteur avec la configuration spécifique.

        Args:
            config: Dictionnaire de configuration spécifique au fournisseur
        """
        pass


    @staticmethod
    def clean_result(text: str) -> str:
        import re
        return re.sub(r'```', '', text)

    @staticmethod
    def get_prompt() -> str:
        return PROMPT