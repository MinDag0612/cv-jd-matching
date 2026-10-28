from abc import ABC, abstractmethod

from app.models.infor_extracted import InforExtractedBase

class BaseExtractionModel(ABC):
    @abstractmethod
    def extract(self, text: str) -> InforExtractedBase:
        raise NotImplementedError
