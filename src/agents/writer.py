from typing import Dict
from src.llm_providers import chat
import json

WRITER_SYS = """
You are a skilled content writer.
Given a structured LinkedIn post plan, generate a polished post in plain text.
Follow these rules:
- Respect the tone, audience, and length from the plan.
- Include the keywords naturally.
- Incorporate news references if use_news is true.
- End with optimized Call-to-Action.
Return the plain text post without any comments.
"""

def generate_post(plan: Dict) -> Dict:
    """
    Generate LinkedIn post text from a structured plan.
    Always returns: {"post": "..."}
    """
    prompt = [
        {"role": "system", "content": WRITER_SYS},
        {"role": "user", "content": json.dumps(plan)},
    ]

    r = chat(prompt)
    raw = r.get("content", "").strip()

    # Ensure output is always {"post": "..."}
    try:
        data = json.loads(raw)
        if isinstance(data, dict) and "post" in data:
            return data
        else:
            return {"post": raw}
    except Exception:
        return {"post": raw}
