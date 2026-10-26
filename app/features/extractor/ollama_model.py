import os
import time

import httpx

from app.models.infor_extracted import InforExtractedBase
from app.features.extractor.model import Model
from app.core.variable import LLMModel, Prompt
from app.models.infor_extracted import (
    InforExtractedBase,
    InforExtractedJD,
    InforExtractedResume,
)
from app.core.config import settings

class OLLAMAModel(Model):
    def __init__(self):
        self.client = httpx.Client(
            base_url=settings.ollama_base_url,
            timeout=settings.ollama_timeout,
        )

    # Retry call function
    def generate_with_retry(self, **kwargs):
        max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            try:
                print(f"Ollama API attempt {attempt}")

                response = self.client.post(
                    "/api/chat",
                    json=kwargs,
                )
                response.raise_for_status()

                result = response.json()
                content = result.get("message", {}).get("content")

                if not content:
                    raise ValueError("Ollama returned an empty response")

                return content

            except (httpx.TimeoutException, httpx.ConnectError):
                if attempt == max_attempts:
                    raise

                wait_seconds = min(2**attempt, 10)

                print(
                    f"Ollama connection/timeout error. "
                    f"Retrying in {wait_seconds}s..."
                )
                time.sleep(wait_seconds)

            except httpx.HTTPStatusError as exc:
                status_code = exc.response.status_code

                # Retry temporary server errors
                if status_code < 500 or attempt == max_attempts:
                    raise

                wait_seconds = min(2**attempt, 10)

                print(
                    f"Ollama server error {status_code}. "
                    f"Retrying in {wait_seconds}s..."
                )
                time.sleep(wait_seconds)

        raise RuntimeError("Ollama request failed")

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
        prompt = Prompt.SYSTEM_RULE + prompt

        response_text = self.generate_with_retry(
            model=LLMModel.OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": (
                        "Extract information from this document: \n\n"
                        f"{parsed_text}"
                    ),
                },
            ],
            format=schema.model_json_schema(),
            options={
                "temperature": 0,
            },
            stream=False,
        )

        return schema.model_validate_json(response_text)
