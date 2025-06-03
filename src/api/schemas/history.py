from datetime import datetime
from typing import Literal, Optional
from pydantic import field_validator, BaseModel, Field


class HistoryMessage(BaseModel):
    role: Literal["user", "assistant", "system"] = Field(
        description="Rôle du message (user/assistant/system)"
    )
    content: str = Field(
        description="Contenu du message",
        min_length=1
    )
    timestamp: Optional[datetime] = Field(
        default=None,
        description="Timestamp du message (optionnel)"
    )

    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        if not v.strip():
            raise ValueError("Le contenu du message ne peut pas être vide")
        return v.strip()