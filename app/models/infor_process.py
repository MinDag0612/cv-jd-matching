from typing import Any
from pydantic import BaseModel

from app.models.infor_commend import CommendResponse

class ProcessorFileResponse(BaseModel):
    filename: str | None
    parsed_text: str
    information: dict[str, Any]

class ResultCompareResponse(BaseModel):
    total_score: float
    list_commend: dict[str, CommendResponse]