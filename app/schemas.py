from pydantic import BaseModel
from typing import Optional, Dict, Any

class AgentRouterConfig(BaseModel):
    provider: str
    model: str
    api_key: Optional[str]

class ProjectAnalysis(BaseModel):
    file_count: int
    loc: int
    languages: Dict[str, int]
    files: Dict[str, int]  # filename -> size
