from fastapi import APIRouter, File, Form, UploadFile, Depends
from app.core.dependencies import get_processor

from app.features.processing.service import ProcessingService
from app.models.infor_process import ProcessorFileResponse
from app.models.infor_process import ResultCompareResponse
from app.models.infor_extracted import InforExtractedJD, InforExtractedResume

router = APIRouter(prefix="/extractor", tags=["Processor"])


@router.post("/extract")
def extract_text(
    request: str,
    is_resume: bool = Form(False),
    processor: ProcessingService = Depends(get_processor)
) -> dict:
    return processor.process_text(request, is_resume)


@router.post("/extract-file", response_model=ProcessorFileResponse)
def parse_and_extract(
    file: UploadFile = File(...),
    is_resume: bool = Form(False),
    processor: ProcessingService = Depends(get_processor)
) -> dict:
    return processor.process_file(file, is_resume)

@router.post("/compare", response_model=ResultCompareResponse)
def compare(
    cv_data: InforExtractedResume,
    jd_data: InforExtractedJD,
    processor: ProcessingService = Depends(get_processor)
) -> dict:
    return processor.compare(
        cv_data=cv_data,
        jd_data=jd_data
    )