from abc import ABC, abstractmethod
from typing import List

class EmbeddingPort(ABC):
    """Port pour la vectorisation de textes"""
    
    @abstractmethod
    def encode(self, texts: List[str]) -> List[List[float]]:
        """
        Encode une liste de textes en vecteurs
        
        Args:
            texts: Liste des textes à encoder
            
        Returns:
            Liste des vecteurs d'embedding
        """
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """
        Retourne le nom du modèle utilisé
        
        Returns:
            Nom du modèle
        """
        pass
