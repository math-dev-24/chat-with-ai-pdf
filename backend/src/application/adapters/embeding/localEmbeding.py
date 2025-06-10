from sentence_transformers import SentenceTransformer
from typing import List
from src.domain.ports.embeding import EmbeddingPort

class LocalEmbeddingAdapter(EmbeddingPort):
    """Adaptateur local pour la vectorisation utilisant SentenceTransformer"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialise l'adaptateur avec un modèle spécifique
        
        Args:
            model_name: Nom du modèle SentenceTransformer à utiliser
        """
        self.model = SentenceTransformer(model_name)
        self._model_name = model_name
        
    def encode(self, texts: List[str]) -> List[List[float]]:
        """
        Encode une liste de textes en vecteurs
        
        Args:
            texts: Liste des textes à encoder
            
        Returns:
            Liste des vecteurs d'embedding
        """
        return self.model.encode(texts).tolist()
    
    def get_model_name(self) -> str:
        """
        Retourne le nom du modèle utilisé
        
        Returns:
            Nom du modèle
        """
        return self._model_name
