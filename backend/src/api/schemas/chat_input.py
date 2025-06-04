from typing import List, Optional, Dict
from pydantic import BaseModel, Field, field_validator
from src.api.schemas.history import HistoryMessage


class AskDataInput(BaseModel):
    question: str = Field(
        description="Question text",
        min_length=1,
        max_length=250,
    )
    historics: List[HistoryMessage] = Field(
        default=[],
        description="Historic des messages messages",
        max_length=50
    )

    # Optional
    max_context_length: int = Field(
        default=4000,
        description="Longueur maximale du contexte pour la recherche",
        ge=1000,
        le=8000
    )
    prefer_chapters: bool = Field(
        default=True,
        description="Privilégier la recherche par chapitres"
    )
    pdf_filter: Optional[str] = Field(
        default=None,
        description="Filtrer par nom de PDF spécifique"
    )

    @field_validator('question')
    @classmethod
    def validate_question(cls, v):
        if not v.strip():
            raise ValueError("La question ne peut pas être vide")
        return v.strip()

    def get_formatted_history(self) -> List[Dict[str, str]]:
        """
        Retourne l'historique au format liste de dict pour intégration facile dans les prompts
        Format: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
        """
        formatted: List[Dict[str, str]] = []

        for msg in self.historics:
            formatted.append({
                "role": msg.role,
                "content": msg.content
            })

        return formatted
