from app.features.parser.parser import Parser
from fastapi import UploadFile
from io import BytesIO
from pypdf import PdfReader

class PDFParser(Parser):
    @staticmethod
    def parse(file: UploadFile) -> str:
        content = file.file.read()
        reader = PdfReader(BytesIO(content))

        pages = [
            page.extract_text() or ""
            for page in reader.pages
        ]

        return "\n".join(pages)
