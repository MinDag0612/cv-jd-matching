from app.models.infor_extracted import InforExtractedBase
from app.features.extractor.model import Model

class Extractor:
    def __init__(self):
        inforExtract: type[InforExtractedBase]
        model: Model
        
        