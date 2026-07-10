import os

import httpx

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_PROPOSAL_MODEL", "qwen3:1.7b")
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "120"))


class OllamaUnavailableError(Exception):
    """Raised when Ollama can't be reached or times out."""


def generate_with_ollama(prompt: str) -> str:
    """
    Send a prompt to the local Ollama server and return the generated text.
    Raises OllamaUnavailableError on any failure so callers can fall back
    to the static template instead of crashing the request.
    """
    try:
        response = httpx.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "keep_alive": "5m",
                "think": False,
                "options": {
                    "temperature": 0.4,
                },
            },
            timeout=OLLAMA_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        text = data.get("response", "").strip()

        if not text:
            raise OllamaUnavailableError("Ollama returned an empty response")

        return text

    except httpx.RequestError as exc:
        raise OllamaUnavailableError(f"Could not reach Ollama: {exc}") from exc
    except httpx.HTTPStatusError as exc:
        raise OllamaUnavailableError(f"Ollama returned an error: {exc}") from exc
