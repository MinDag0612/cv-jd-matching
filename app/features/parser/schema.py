from pydantic import BaseModel


class ParseResponse(BaseModel):
    filename: str | None
    text: str
