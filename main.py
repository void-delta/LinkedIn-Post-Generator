"""
app.py
Streamlit app for LinkedIn Post Generator (3 posts, card layout, usage & moderation)
"""
import streamlit as st
import json
import os

# Local imports
from src.agents.writer import generate_post
from src.utils.moderation import moderate_post
from src.llm_providers import chat
from src.utils.cost import estimate_cost
from src.utils.text import clean_text
from src.agents.hashtags import generate_hashtags

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="💼",
    layout="wide",
)

# --- Secrets Handling ---
# ✅ Safely load from .streamlit/secrets.toml
MODEL_NAME = st.secrets.get("MODEL_NAME", "gemini-1.5-flash")
LLM_PROVIDER = st.secrets.get("LLM_PROVIDER", "gemini")
TEMPERATURE = float(st.secrets.get("TEMPERATURE", "0.7"))
MAX_TOKENS = int(st.secrets.get("MAX_TOKENS", "1000"))

# API keys
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY")
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY")
ANTHROPIC_API_KEY = st.secrets.get("ANTHROPIC_API_KEY")
NEWS_API_KEY = st.secrets.get("NEWS_API_KEY")

# Debug (optional)
# st.write("🔑 GEMINI key loaded?", GEMINI_API_KEY is not None)

# --- UI ---
st.title("💼 LinkedIn Post Generator")
st.write("Craft professional LinkedIn posts with Agentic AI.")


# --- Inputs ---
col1, col2 = st.columns(2)

with col1:
    topic = st.text_input("🔑 Topic", placeholder="e.g., AI in Marketing")
    tone = st.selectbox(
        "🎙️ Tone",
        ["Professional", "Casual", "Inspirational", "Educational"],
        index=0,
    )
    audience = st.selectbox(
        "👥 Audience",
        ["Professionals", "Students", "Engineers", "General Public", "C-Suite Executives"],
        index=0,
    )
    cta = st.text_input(
        "📢 Call To Action (CTA)",
        placeholder="If this resonated, share your thoughts below!",
        value="If this resonated, share your thoughts below!",
    )

with col2:
    length = st.selectbox(
        "📏 Length",
        ["Very Short", "Short", "Medium", "Long", "Very Long"],
        index=1,
    )
    outline = st.multiselect(
        "📝 Outline (select sections to include)",
        ["Hook", "Key Insight", "Supporting Example", "CTA"],
        default=["Hook", "Key Insight", "CTA"],
    )
    keywords = st.text_input(
        "🏷️ Keywords (comma-separated)",
        placeholder="e.g., AI, marketing, business growth",
        value="AI, Marketing",
    )
    use_news = st.toggle("📰 Include Recent News?", value=False)


st.markdown("<br>", unsafe_allow_html=True)


# --- Generate ---
if st.button("🚀 Generate Posts"):
    with st.spinner("Generating your LinkedIn posts..."):

        # Plan dict passed into writer
        plan_data = {
            "topic": topic,
            "tone": tone,
            "audience": audience,
            "length": length,
            "outline": outline,
            "use_news": use_news,
            "keywords": [k.strip() for k in keywords.split(",") if k.strip()],
            "cta": cta,
        }

        posts_data = []
        usage_data = {"input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "model": ""}

        for _ in range(3):
            post_result = generate_post(plan_data)
            posts_data.append(clean_text(post_result.get("post", "")))

            if "cost" in post_result:
                usage_data = post_result["cost"]

        # Moderation pass
        moderation_results = [moderate_post(p) for p in posts_data]

    st.subheader("✍️ Generated Posts")

    # --- CSS for Cards ---
    st.markdown("""
        <style>
        .post-card {
            background-color: #1e1e1e;
            color: #f0f0f0;
            border-radius: 12px;
            padding: 15px;
            margin: 5px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            position: relative;
            font-family: monospace;
        }
        .post-card h4 {
            margin-top: 0;
            color: #F63366;
        }
        .post-card pre {
            background-color: #2b2b2b;
            padding: 10px;
            border-radius: 8px;
            overflow-x: auto;
            max-height: 300px;
        }
        .copy-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            background-color: #ffd700;
            color: #000;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- 3-column layout for cards ---
    cols = st.columns(3)
    for i, (col, post, moderation) in enumerate(zip(cols, posts_data, moderation_results)):
        with col:
            # Ensure post text is safe (moderation already applied)
            post_text = moderation if isinstance(moderation, str) else str(moderation)
            post_html = post_text.replace("\n", "<br>")
            hashtags = generate_hashtags(post_text)

            st.markdown(
                f"""
                <div class="post-card">
                    <h4>Post {i+1}</h4>
                    <div id="post-{i}">{post_html}</div>
                    <div id="post-{i}">{hashtags}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )