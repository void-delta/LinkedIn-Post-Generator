# src/agents/guardrail.py

from src.utils.moderation import moderate_post

def guard(text: str) -> str:
    """
    Runs moderation checks on the text.
    Always returns only the final LinkedIn post text,
    or 'Not Safe to post' if unsafe.
    """
    return moderate_post(text)
