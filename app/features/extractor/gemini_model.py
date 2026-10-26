from app.models.infor_extracted import InforExtractedBase
from app.features.extractor.model import Model
from app.core.variable import LLMModel, Prompt
from app.models.infor_extracted import InforExtractedBase, InforExtractedJD, InforExtractedResume

from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
import os
import time

load_dotenv()

class GEMINIModel(Model):
    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )
        
    # Retry call function
    # GEMINI has a lot request
    def generate_with_retry(self, **kwargs):
        attempt = 0

        while True:
            attempt += 1

            try:
                print(f"Gemini API attempt {attempt}")
                return self.client.models.generate_content(**kwargs)

            except errors.ServerError as exc:
                if exc.code != 503:
                    raise

                wait_seconds = min(5 * attempt, 60)
                print(
                    f"Gemini API error 503. "
                    f"Retrying in {wait_seconds}s..."
                )
                time.sleep(wait_seconds)
                
            except errors.ClientError as exc:
                if exc.code == 429:
                    raise RuntimeError(
                        "Gemini API is out of quota. "
                        "Wait for quota recover."
                    ) from exc
                raise
        
    def extract(
        self, 
        parsed_text: str, 
        is_resume: bool = False,
    ) -> InforExtractedBase:
        
        schema = InforExtractedResume if is_resume else InforExtractedJD
        prompt = (
            Prompt.PROMPT_EXTRACT_INFOR_RESUME.value
            if is_resume
            else Prompt.PROMPT_EXTRACT_INFOR_JD.value
        )
        
        response = self.generate_with_retry(
            model=LLMModel.GEMINI_FLASH.value,
            contents=[
                f"{prompt}\n\nResume/JD text:\n{parsed_text}"
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )

        if not response.text:
            raise ValueError("Failed to extract information")

        return schema.model_validate_json(response.text)

