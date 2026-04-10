import os

import requests
from fastapi import Body, FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"
OLLAMA_TIMEOUT_SECONDS = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "60"))


class PromptModel(BaseModel):
    prompt: str = Field(..., min_length=1, description="SMS text to classify")


@app.post("/generate")
def generate_text(prompt: PromptModel = Body()):
    """
    Классифицирует SMS-сообщение как спам или не спам с использованием LLM.

    Эндпоинт принимает `prompt`, формирует системный промпт и проксирует
    запрос к локальному сервису Ollama (модель qwen2.5:0.5b).
    """
    user_message = prompt.prompt.strip()
    if not user_message:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Field `prompt` must not be empty.",
        )

    system_prompt = """
You classify one SMS message as spam or not spam.
Return only valid JSON (no markdown, no comments, no extra text):
{"is_spam": true/false, "spam_topic": "lottery|phishing|ads|scam|"}

Rules:
1) If message is spam: is_spam=true and spam_topic is one of lottery/phishing/ads/scam.
2) If message is not spam: is_spam=false and spam_topic is an empty string.
3) Never output keys other than is_spam and spam_topic.
4) Be robust to typos and broken English.

SMS:
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": f"{system_prompt}{user_message}",
        "stream": False,
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=OLLAMA_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Ollama is unavailable: {exc}",
        ) from exc

    if response.status_code >= 400:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Ollama returned HTTP {response.status_code}: {response.text}",
        )

    try:
        ollama_json = response.json()
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Ollama returned invalid JSON.",
        ) from exc

    if "response" not in ollama_json:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unexpected Ollama response: missing `response` field.",
        )

    return ollama_json
