import os
import re
from typing import Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types


class TaskEvaluation(BaseModel):
    is_complete: bool = Field(description="True if task requirements are completely satisfied")
    score: int = Field(ge=1, le=10, description="Quality rating from 1 to 10")
    feedback: str = Field(description="Constructive technical feedback")


class GeminiStructuredAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.environ.get("GEMINI_API_KEY"))

    def evaluate_task(self, requirements: str, implementation: str) -> TaskEvaluation:
        prompt = (
            f"Requirements:\n{requirements}\n\n"
            f"Implementation:\n{implementation}\n\n"
            "Evaluate whether the implementation satisfies the requirements."
        )

        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=TaskEvaluation,
            temperature=0.1,
        )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )

        raw_text = response.text or ""
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_text.strip(), flags=re.MULTILINE)
        return TaskEvaluation.model_validate_json(cleaned)
