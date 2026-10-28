from fastapi import HTTPException, UploadFile

from app.features.parsing.factory import ParserFactory


def parse_uploaded_file(file: UploadFile) -> str:
    try:
        parser = ParserFactory.get_factory(file)
    except ValueError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc
    return parser(file)
