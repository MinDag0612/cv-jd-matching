from app.features.extraction.ollama_model import OllamaModel


def extract_information(text: str, is_resume: bool) -> dict:
    model = OllamaModel()
    try:
        result = model.extract(parsed_text=text, is_resume=is_resume)
        return result.model_dump()
    finally:
        model.client.close()
