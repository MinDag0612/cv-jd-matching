from pathlib import Path

from fastapi import UploadFile
from typing import Callable

from app.features.parser.docx_parser import DOCXParser
from app.features.parser.pdf_parser import PDFParser

class ParserFactory:
    @staticmethod
    def get_factory(file: UploadFile) -> Callable[[UploadFile], str]:
        extension = Path(file.filename or "").suffix.lower()

        if extension == ".pdf":
            return PDFParser.parse

        if extension == ".docx":
            return DOCXParser.parse

        raise ValueError(f"Unsupported file extension: {extension}")
