from fastapi import APIRouter, File, Form, UploadFile

from app.features.processor.processor import Processor
from app.features.processor.schema import ProcessorFileResponse

router = APIRouter(prefix="/extractor", tags=["Processor"])
processor = Processor()


@router.post("/extract")
def extract_text(
    request: str,
    is_resume: bool = Form(False),
) -> dict:
    return processor.process_text(request, is_resume)


@router.post("/extract-file", response_model=ProcessorFileResponse)
def parse_and_extract(
    file: UploadFile = File(...),
    is_resume: bool = Form(False),
) -> dict:
    return processor.process_file(file, is_resume)
