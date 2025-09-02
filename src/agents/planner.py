from typing import Dict
from src.llm_providers import chat

PLANNER_SYS = """
You are a planning agent for LinkedIn posts.
Given a topic and user preferences, create a JSON plan with these keys:
- tone: the voice/style to use
- audience: the audience targeted
- length: short/medium/long
- outline: array of section bullets (3–5 items)
- use_news: boolean (true if recent events/news would improve credibility)
- keywords: array of 3–6 important keywords/hashtags
- cta: a strong call-to-action (string)

Return only valid compact JSON (no commentary).
"""


def plan(topic: str, tone: str, audience: str, length: str) -> Dict:
    """
    Generate a structured post plan.
    Fallbacks to defaults if JSON parsing fails.
    """
    prompt = [
        {"role": "system", "content": PLANNER_SYS},
        {
            "role": "user",
            "content": f"Topic: {topic}\nTone: {tone}\nAudience: {audience}\nLength: {length}\n"
                       "Output JSON only.",
        },
    ]

    r = chat(prompt)
    raw = r["content"]

    import json

    try:
        data = json.loads(raw.strip())
    except Exception:
        # Default fallback plan
        data = {
            "tone": tone,
            "audience": audience,
            "length": length,
            "outline": ["Hook", "Key Insight", "Supporting Example", "CTA"],
            "use_news": False,
            "keywords": [topic],
            "cta": "If this resonated, share your thoughts below!",
        }

    return data
