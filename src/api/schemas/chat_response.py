from typing import Optional, List
from pydantic import BaseModel, Field
from src.api.schemas.history import HistoryMessage


class AskDataResponse(BaseModel):
    """Modèle pour les réponses"""
    question: str = Field(description="Question posée")
    response: str = Field(description="Réponse de l'IA")
    context: str = Field(description="Contexte utilisé pour la réponse")
    context_length: int = Field(description="Longueur du contexte")
    sources_count: int = Field(description="Nombre de sources utilisées")
    processing_time: Optional[float] = Field(
        default=None,
        description="Temps de traitement en secondes"
    )
    updated_history: List[HistoryMessage] = Field(
        description="Historique mis à jour avec la nouvelle réponse"
    )
