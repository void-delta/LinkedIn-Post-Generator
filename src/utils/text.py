import re
import json

def clean_text(raw: str) -> str:
    """
    Extracts and returns only the post text from a JSON-wrapped string.
    
    Example input:
    '```json { "post": "Hello world!" } ```'
    
    Returns:
    'Hello world!'
    """
    if not raw:
        return ""

    # Remove markdown fences like ```json ... ```
    cleaned = re.sub(r"```(?:json)?", "", raw, flags=re.IGNORECASE).strip("` \n")

    try:
        # Parse JSON if it's valid
        data = json.loads(cleaned)
        if isinstance(data, dict) and "post" in data:
            return data["post"].strip()
    except Exception:
        pass

    # Fallback: try regex to capture post inside { "post": "..." }
    match = re.search(r'\"post\"\s*:\s*\"(.*)\"', cleaned, re.DOTALL)
    if match:
        return match.group(1).encode("utf-8").decode("unicode_escape").strip()

    # If nothing worked, just return the raw cleaned string
    return cleaned.strip()
