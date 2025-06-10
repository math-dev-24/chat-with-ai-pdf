from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi import UploadFile


class LoadAllPdfInput(BaseModel):
    user_id: str = Field(
        description="ID unique de l'utilisateur",
        min_length=1
    )
    custom_pdf_path: Optional[str] = Field(
        description="Chemin personnalisé vers le dossier contenant les PDFs",
        default=None
    )

class ProcessPdfByFileInput(BaseModel):
    user_id: str = Field(
        description="ID unique de l'utilisateur",
        min_length=1
    )
    custom_pdf_path: Optional[str] = Field(
        description="Chemin personnalisé vers le dossier contenant les PDFs",
        default=None
    )
    max_files: int = Field(
        description="Nombre maximum de fichiers à traiter",
        default=5
    )

class UploadDocumentsInput(BaseModel):
    user_id: str = Field(
        description="ID unique de l'utilisateur",
        min_length=1
    )
    files: List[UploadFile] = Field(
        description="Fichiers à télécharger"
    )

class DeleteFileInput(BaseModel):
    user_id: str = Field(
        description="ID unique de l'utilisateur",
        min_length=1
    )
    file_name: str = Field(
        description="Nom du fichier à supprimer",
        min_length=1
    )