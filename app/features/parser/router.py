from fastapi import APIRouter, File, UploadFile

from app.features.parser.parser_service import parse_uploaded_file
from app.features.parser.schema import ParseResponse


router = APIRouter(prefix="/parser", tags=["Parser"])


@router.post("/parse", response_model=ParseResponse)
def parse_file(file: UploadFile = File(...)) -> ParseResponse:
    return ParseResponse(filename=file.filename, text=parse_uploaded_file(file))
