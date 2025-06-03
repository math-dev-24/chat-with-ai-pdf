from abc import ABC, abstractmethod
from typing import List, Dict, Any


class EmbeddingConnector(ABC):
    """Interface abstraite pour les générateurs d'embeddings."""

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialise le générateur d'embeddings.

        Args:
            config: Configuration (modèle, dimensions, etc.)
        """
        pass

    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        """
        Génère un embedding pour un texte donné.

        Args:
            text: Texte à vectoriser

        Returns:
            Vecteur d'embedding
        """
        pass

    @abstractmethod
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Génère des embeddings pour une liste de textes (plus efficace).

        Args:
            texts: Liste des textes à vectoriser

        Returns:
            Liste des vecteurs d'embedding
        """
        pass

    @abstractmethod
    def get_dimension(self) -> int:
        """
        Retourne la dimension des embeddings générés.

        Returns:
            Dimension du vecteur
        """
        pass

    @abstractmethod
    def get_cost_estimation(self, total_tokens: int) -> float:
        """
        Retourne le prix

        Returns:
            Prix de l'embeding
        """