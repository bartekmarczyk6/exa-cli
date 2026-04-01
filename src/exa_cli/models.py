# Pydantic models can be added here if needed for strict validation
# Currently, the CLI uses raw dicts for flexibility, but this file is included
# per the project structure requirements.

from pydantic import BaseModel
from typing import List, Optional

class SearchResult(BaseModel):
    title: Optional[str] = None
    url: str
    publishedDate: Optional[str] = None
    score: Optional[float] = None
    text: Optional[str] = None
    highlights: Optional[List[str]] = None
    summary: Optional[str] = None

class SearchResponse(BaseModel):
    results: List[SearchResult]
