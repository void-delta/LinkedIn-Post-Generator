"""
moderation.py
Runs safety and content moderation checks on LLM outputs
using Gemini (Google AI) with GEMINI_API_KEY.
"""

import google.generativeai as genai
from src.config import settings

# Configure Gemini
genai.configure(api_key=settings.gemini_key)

MODERATION_MODEL = "gemini-1.5-flash-8b"

GUARDRAIL_SYS = """
You are a moderation agent for LinkedIn posts.

Definitions:
- SAFE = normal professional, educational, or marketing content.
- UNSAFE = contains hate speech, violence, explicit sexual content, terrorism, or encouragement of self-harm.

Rules:
- If SAFE: return the post text exactly as it is, with no extra formatting.
- If UNSAFE: rewrite the text into a safe, professional LinkedIn post.
- Do not add explanations, metadata, or JSON. Only return the final post text.
"""

def moderate_post(text) -> str:
    """
    Moderates a LinkedIn post using Gemini directly.
    Returns only the post if safe, otherwise rewritten safe text.
    Accepts either a raw string or a dict {"post": "..."}.
    """
    # Unwrap dict if needed
    if isinstance(text, dict) and "post" in text:
        text = text["post"]

    try:
        response = genai.GenerativeModel(MODERATION_MODEL).generate_content(
            [
                {"role": "system", "parts": [GUARDRAIL_SYS]},
                {"role": "user", "parts": [text]},
            ],
            generation_config={"temperature": 0.2},
        )

        # Extract the plain text response
        if response and response.candidates:
            return response.candidates[0].content.parts[0].text.strip()

        return "Not Safe to post"

    except Exception:
        return "Not Safe to post"


if __name__ == "__main__":
    safe = {"post": "AI is transforming the future of healthcare in exciting ways."}
    unsafe = {"post": "This post promotes hate and violence."}

    print("Safe test ->", moderate_post(safe))
    print("Unsafe test ->", moderate_post(unsafe))
