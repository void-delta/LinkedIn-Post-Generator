"""
app.py
Streamlit app for LinkedIn Post Generator (3 posts, card layout, usage & moderation)
"""

import streamlit as st
import json
from src.agents.planner import plan
from src.agents.writer import generate_post
from src.utils.moderation import moderate_post
from src.llm_providers import chat
from src.utils.cost import estimate_cost
from src.utils.text import clean_text
from dotenv import load_dotenv
load_dotenv()
import os
print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))
print("HF_API_KEY:", os.getenv("HF_API_KEY"))


st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="💼",
    layout="wide",
)

st.title("💼 LinkedIn Post Generator")
st.write("Craft professional LinkedIn posts with AI assistance.")

# --- Inputs ---
# Two-column layout for inputs
col1, col2 = st.columns(2)

with col1:
    topic = st.text_input("🔑 Topic", placeholder="e.g., AI in Marketing")
    tone = st.selectbox(
        "🎙️ Tone",
        ["professional", "casual", "inspirational", "educational"],
        index=0,
    )
    audience = st.selectbox(
        "👥 Audience",
        ["Marketing Executives", "Students", "Engineers", "General Public"],
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
        ["short", "medium", "long"],
        index=1,
    )
    outline = st.multiselect(
        "📝 Outline (select sections to include)",
        ["Hook", "Key Insight", "Supporting Example", "CTA"],
        default=["Hook", "Key Insight", "Supporting Example", "CTA"],
    )
    keywords = st.text_input(
        "🏷️ Keywords (comma-separated)",
        placeholder="e.g., AI, marketing, business growth",
        value="AI",
    )
    use_news = st.toggle("📰 Include Recent News?", value=False)
    

# Optional: add some spacing between columns for a nicer look
st.markdown("<br>", unsafe_allow_html=True)


# --- Generate ---
if st.button("🚀 Generate Posts"):
    with st.spinner("Generating your LinkedIn posts..."):

        # Build plan dict
        plan_data = {
            "tone": tone,
            "audience": audience,
            "length": length,
            "outline": outline,
            "use_news": use_news,
            "keywords": [k.strip() for k in keywords.split(",") if k.strip()],
            "cta": cta,
        }

        # Generate 3 posts
        posts_data = []
        usage_data = {"input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "model": ""}
        for _ in range(3):
            post_result = generate_post(plan_data)
            posts_data.append(clean_text(post_result.get("post", "")))

            # Aggregate usage and cost
            if "cost" in post_result:
                usage_data = post_result["cost"]

        # Run moderation on each post
        moderation_results = [moderate_post({"post": p}) for p in posts_data]

    st.subheader("✍️ Generated Posts")

    # CSS for card style
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
            color: #ffd700;
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

    # 3-column layout
    cols = st.columns(3)
    for i, (col, post, moderation) in enumerate(zip(cols, posts_data, moderation_results)):
        with col:
            moderation_json = json.dumps(moderation, indent=2)
            st.markdown(f"""
                <div class="post-card">
                    <button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById('mod-{i}').innerText)">Copy JSON</button>
                    <h4>Post</h4>
                    <pre id="mod-{i}">{moderation_json}</pre>
                </div>
            """, unsafe_allow_html=True)



    st.subheader("📊 Usage & Cost")
    st.json(usage_data)
