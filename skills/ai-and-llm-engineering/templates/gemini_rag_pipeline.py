import os
from typing import List, Dict, Optional
from google import genai
from google.genai import types


class GroundedRAGPipeline:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.environ.get("GEMINI_API_KEY"))

    def synthesize_answer(self, question: str, source_chunks: List[Dict[str, str]]) -> str:
        formatted_context = "\n\n".join(
            f"[Source ID: {c['id']}]\n{c['content']}" for c in source_chunks
        )

        prompt = (
            "You are a factual synthesis engine. Answer the question using ONLY the provided sources.\n"
            "Cite every fact using [Source ID: ...]. If the sources do not contain the answer, state that.\n\n"
            f"Sources:\n{formatted_context}\n\n"
            f"Question: {question}"
        )

        config = types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=1024,
        )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )
        return response.text or ""
