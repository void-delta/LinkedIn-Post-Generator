# src/llm_providers.py

from typing import List, Dict, Any
from litellm import completion
from src.config import settings

def chat(
    messages: List[Dict[str, str]],
    *,
    temperature: float | None = None,
    max_tokens: int | None = None,
    model: str | None = None,
) -> Dict[str, Any]:
    """
    Unified chat interface across Gemini and Hugging Face.
    Uses LiteLLM under the hood.
    """

    provider = settings.provider.lower()
    chosen_model = model or settings.model_name

    try:
        resp = completion(
            model=chosen_model,
            messages=messages,
            temperature=temperature or settings.temperature,
            max_tokens=max_tokens or settings.max_tokens,
            api_key=settings.gemini_key if provider == "gemini" else settings.hf_key,
        )
    except Exception as e:
        # Fallback: if Gemini fails and HF key exists
        if provider == "gemini" and settings.hf_key:
            resp = completion(
                model="huggingface/mistralai/Mixtral-8x7B-Instruct",
                messages=messages,
                temperature=temperature or settings.temperature,
                max_tokens=max_tokens or settings.max_tokens,
                api_key=settings.hf_key,
            )
        else:
            raise RuntimeError(f"LLM call failed: {e}")

    content = resp.choices[0].message["content"]
    usage = getattr(resp, "usage", None) or {}

    return {"content": content, "usage": usage}
