# src/agents/graph.py

from src.agents import planner, writer, guardrails, tools

def run_pipeline(topic: str, tone: str, audience: str, length: str) -> dict:
    """
    Orchestrates the workflow:
    planner -> optional news -> writer -> guardrail
    Returns structured output with intermediate steps.
    """
    # Step 1: Planner
    plan = planner.plan(topic, tone, audience, length)

    # Step 2: Optional news tool
    news = []
    if plan.get("use_news"):
        news = tools.get_recent_news(topic, limit=3)

    # Step 3: Writer
    draft = writer.write(plan, news=news)

    # Step 4: Guardrail
    safe_text = guardrails.guard(draft)

    return {
        "plan": plan,
        "news": news,
        "draft": draft,
        "final": safe_text,
    }
