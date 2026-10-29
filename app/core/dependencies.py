from fastapi import Request

from app.features.processing.service import ProcessingService

def get_processor(request: Request) -> ProcessingService:
    return request.app.state.processor