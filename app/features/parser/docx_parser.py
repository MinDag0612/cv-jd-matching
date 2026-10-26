from app.features.parser.parser import Parser
from fastapi import UploadFile
from io import BytesIO
from docx import Document

class DOCXParser(Parser):
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