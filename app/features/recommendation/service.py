import time

import httpx

from app.core.config import settings
from app.core.variable import LLMModel, Prompt
from app.models.infor_commend import CommendResponse
from app.models.match_feature import MatchFeature


class RecommendationService:
    def __init__(self):
        self.client = httpx.Client(
            base_url=settings.ollama_base_url,
            timeout=settings.ollama_timeout,
        )

    def generate_with_retry(self, **kwargs) -> str:
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

                if status_code < 500 or attempt == max_attempts:
                    raise

                wait_seconds = min(2**attempt, 10)
                print(
                    f"Ollama server error {status_code}. "
                    f"Retrying in {wait_seconds}s..."
                )
                time.sleep(wait_seconds)

        raise RuntimeError("Ollama request failed")

    def recommend(self, match_feature: MatchFeature) -> CommendResponse:
        prompt = Prompt.PROMPT_MATCH_EVALUATION

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
                        f"Feature type: {match_feature.feature_type}\n"
                        f"CV feature: {match_feature.cv_text}\n"
                        f"Job description feature: {match_feature.jd_text}"
                    ),
                },
            ],
            format=CommendResponse.model_json_schema(),
            options={
                "temperature": 0,
            },
            stream=False,
        )

        return CommendResponse.model_validate_json(response_text)