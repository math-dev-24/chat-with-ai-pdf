from typing import Optional
from pydantic import BaseModel


class PDFInfo(BaseModel):
    name: str
    path: str
    size: int
    chapters: Optional[int] = None

class PDFUploadResponse(BaseModel):
    success: bool
    message: str
    pdf_name: str
    chapters_count: int