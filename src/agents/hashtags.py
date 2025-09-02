from src.llm_providers import chat

HASHTAG_SYS = """
You are a hashtag generator for LinkedIn posts.
Given a LinkedIn post, return 5-10 optimized hashtags.
Rules:
- Use only relevant hashtags.
- No numbering, no explanations.
- Return strictly as plain text in a single line, separated by spaces.
Example: #AI #Marketing #LinkedIn
"""

def generate_hashtags(post_text: str) -> str:
    """
    Generate hashtags for a LinkedIn post using the LLM.
    Returns a plain text string like: "#AI #Marketing #Business"
    """
    prompt = [
        {"role": "system", "content": HASHTAG_SYS},
        {"role": "user", "content": post_text},
    ]

    r = chat(prompt)
    raw = r.get("content", "").strip()

    # Just return the hashtags as plain text
    return raw
