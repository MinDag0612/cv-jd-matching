from app.features.extractor.ollama_model import OLLAMAModel


def extract_information(text: str, is_resume: bool) -> dict:
    model = OLLAMAModel()
    try:
        result = model.extract(parsed_text=text, is_resume=is_resume)
        return result.model_dump()
    finally:
        model.client.close()
