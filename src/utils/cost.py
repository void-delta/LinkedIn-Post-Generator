# src/utils/cost.py
from typing import Dict, Any

# Real Google AI Studio rates (USD per 1k tokens)
_GEMINI_RATES = {
    "gemini-1.5-flash": {"input_per_1k": 0.000075, "output_per_1k": 0.0003},
    "gemini-1.5-pro": {"input_per_1k": 0.00125, "output_per_1k": 0.005},
}

def _normalize_model_key(model: str) -> str:
    m = (model or "").lower()
    if "flash" in m:
        return "gemini-1.5-flash"
    if "pro" in m:
        return "gemini-1.5-pro"
    return "gemini-1.5-flash"  # default to Flash if unspecified

def estimate_cost(model: str, usage_metadata: Any) -> Dict[str, Any]:
    """
    Estimate cost directly from Gemini's usage_metadata.
    usage_metadata is typically response.usage_metadata from google-generativeai.

    Example structure:
    {
        "prompt_token_count": 120,
        "candidates_token_count": 380,
        "total_token_count": 500
    }
    """
    key = _normalize_model_key(model)
    rates = _GEMINI_RATES[key]

    input_tokens = int(getattr(usage_metadata, "prompt_token_count", 0) or 0)
    output_tokens = int(getattr(usage_metadata, "candidates_token_count", 0) or 0)

    cost = (input_tokens / 1000.0) * rates["input_per_1k"] + \
           (output_tokens / 1000.0) * rates["output_per_1k"]

    return {
        "model": key,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": round(cost, 8),
    }

if __name__ == "__main__":
    # Example with fake usage metadata object
    class FakeUsage:
        prompt_token_count = 120
        candidates_token_count = 380
        total_token_count = 500

    usage = FakeUsage()
    print(estimate_cost("gemini-1.5-flash", usage))
