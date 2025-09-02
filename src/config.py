import os
from dataclasses import dataclass
from typing import Optional
import streamlit as st


@dataclass
class Settings:
    # Default to Gemini (student-friendly, free daily quota)
    model_name: str = st.secrets.get("MODEL_NAME", "gemini-1.5-flash")
    provider: str = st.secrets.get("LLM_PROVIDER", "gemini")

    # Sampling params
    temperature: float = float(st.secrets.get("TEMPERATURE", 0.7))
    max_tokens: int = int(st.secrets.get("MAX_TOKENS", 1000))

    # API keys
    gemini_key: Optional[str] = st.secrets.get("GEMINI_API_KEY")      # Google AI Studio
    hf_key: Optional[str] = st.secrets.get("HUGGINGFACE_API_KEY")     # Hugging Face Inference

    # Optional OpenAI/Anthropic (not default, but supported if you add keys)
    openai_key: Optional[str] = st.secrets.get("OPENAI_API_KEY")
    anthropic_key: Optional[str] = st.secrets.get("ANTHROPIC_API_KEY")

    # Optional NewsAPI tool
    news_api_key: Optional[str] = st.secrets.get("NEWS_API_KEY")


settings = Settings()
