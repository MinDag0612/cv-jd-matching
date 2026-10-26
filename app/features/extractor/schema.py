from pydantic import BaseModel, Field

class ExtractRequest(BaseModel):
    text: str = Field(min_length=1)
    is_resume: bool = False
