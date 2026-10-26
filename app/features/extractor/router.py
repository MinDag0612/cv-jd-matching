from fastapi import APIRouter, File, Form, UploadFile

from app.features.extractor.extractor_service import extract_information
from app.features.extractor.schema import ExtractRequest
from app.features.parser.parser_service import parse_uploaded_file

router = APIRouter(prefix="/extractor", tags=["Extractor"])

@router.post("/extract")
def extract_text(request: ExtractRequest) -> dict:
    return extract_information(request.text, request.is_resume)


@router.post("/extract-file")
def parse_and_extract(
    file: UploadFile = File(...),
    is_resume: bool = Form(False),
) -> dict:
    parsed_text = parse_uploaded_file(file)
    information = extract_information(parsed_text, is_resume)
    return {
        "filename": file.filename,
        "parsed_text": parsed_text,
        "information": information,
    }
