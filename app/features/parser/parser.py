from abc import ABC, abstractmethod
from fastapi import UploadFile
from io import BytesIO
from docx import Document
from pypdf import PdfReader


class Parser(ABC):
    @abstractmethod
    def parse(file: UploadFile) -> str:
        pass