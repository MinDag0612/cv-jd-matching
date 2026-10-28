from app.features.parsing.base_parser import BaseParser
from fastapi import UploadFile
from io import BytesIO
from docx import Document

class DOCXParser(BaseParser):
    @staticmethod
    def parse(file: UploadFile) -> str:
        content = file.file.read()
        document = Document(BytesIO(content))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)