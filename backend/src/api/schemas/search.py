from typing import List, Optional
from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    pdf_name: Optional[str] = None
    top_k: int = 5
    prefer_chapters: bool = True

class SearchResponse(BaseModel):
    query: str
    results_count: int
    results: List[dict]