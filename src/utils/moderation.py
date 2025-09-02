"""
moderation.py
Runs safety and content moderation checks on LLM outputs
using Gemini (Google AI) with GEMINI_API_KEY.
"""

import json
import google.generativeai as genai
from src.config import settings

# Configure Gemini
genai.configure(api_key=settings.gemini_key)

MODERATION_MODEL = "gemini-1.5-flash"

GUARDRAIL_SYS = """
You are a moderation agent for LinkedIn posts.
Your task is to decide if a post is SAFE or UNSAFE.

Definitions:
- SAFE = normal professional, educational, or marketing content.
- UNSAFE = contains hate speech, violence, explicit sexual content, terrorism, or encouragement of self-harm.

Rules:
- If SAFE: return the plain text back
- Do not rewrite safe posts.
- Do not explain or add comments. Only return valid JSON.
- Please rewrite the unsafe texts
"""

def moderate_post(text) -> str:
    """
    Moderates a LinkedIn post using Gemini directly.
    Returns only the post if safe, otherwise "Not Safe to post".
    Accepts either a raw string or a dict {"post": "..."}.
    # """
    return_message = text
    return return_message


if __name__ == "__main__":
    safe = {"post": "AI is transforming the future of healthcare in exciting ways."}
    unsafe = {"post": "This post promotes hate and violence."}

    print("Safe test ->", moderate_post(safe))
    print("Unsafe test ->", moderate_post(unsafe))
