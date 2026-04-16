import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tavily import TavilyClient

# ---------- SETUP ----------
load_dotenv()

tavily_client = TavilyClient()

MODEL_INFO = "qwen/qwen3-32b"
MODEL_SCRIPT = "qwen/qwen3-32b"

st.set_page_config(
    page_title="VidAgent AI",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    margin-bottom: 10px;
}
.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}
.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
}
.stTextInput>div>div>input {
    border-radius: 10px;
}
button[kind="primary"] {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- FUNCTIONS ----------
def get_realtime_info(query):
    try:
        response = tavily_client.search(query=query, max_results=3)

        if response and response.get("results"):
            summaries = []
            for r in response["results"]:
                title = r.get("title", "")
                snippet = r.get("snippet", "")
                url = r.get("url", "")
                summaries.append(f"{title}\n{snippet}\n{url}")

            source_info = "\n\n---\n\n".join(summaries)
        else:
            source_info = f"No result updates on {query}"

    except Exception as e:
        st.error(f"Error fetching information: {e}")
        return None

    prompt = f"""
    You are an expert researcher and content creator.

    Generate a clear, engaging 150–200 word summary for: "{query}"

    Only use the provided information.

    Source:
    {source_info}
    """

    try:
        model = ChatGroq(model=MODEL_INFO)
        response = model.invoke(prompt)
        return response.content
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return source_info


def generate_video_script(info_text):
    prompt = f"""
    Create a viral short video script (100–120 words).

    - Start with a strong hook
    - Keep it fast-paced and engaging
    - End with CTA

    Content:
    {info_text}
    """

    try:
        model = ChatGroq(model=MODEL_SCRIPT)
        response = model.invoke(prompt)
        return response.content
    except Exception as e:
        st.error(f"Error generating video script: {e}")
        return None


# ---------- UI ----------
def main():
    st.markdown('<div class="title">🎬 VidAgent AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Turn Real-Time Data into Viral Video Scripts</div>', unsafe_allow_html=True)

    query = st.text_input(
        "🔍 Enter your topic",
        placeholder="e.g. AI trends 2026, IPL news, SpaceX updates..."
    )

    # ---------- GENERATE SUMMARY ----------
    if st.button("🚀 Generate Insights", use_container_width=True):

        if not query:
            st.warning("Please enter a topic")
            return

        with st.spinner("🔎 Fetching real-time data..."):
            info_result = get_realtime_info(query)

        if info_result:
            st.session_state["info_result"] = info_result
            st.session_state.pop("script", None)  # reset old script

    # ---------- SHOW SUMMARY ----------
    if "info_result" in st.session_state:

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Research Summary")
        st.write(st.session_state["info_result"])
        st.markdown('</div>', unsafe_allow_html=True)

        # ---------- GENERATE SCRIPT ----------
        if st.button("🎬 Generate Video Script", use_container_width=True):

            with st.spinner("✍️ Writing viral script..."):
                script = generate_video_script(st.session_state["info_result"])

            if script:
                st.session_state["script"] = script

    # ---------- SHOW SCRIPT ----------
    if "script" in st.session_state:

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎥 Your Video Script")
        st.write(st.session_state["script"])

        st.download_button(
            "⬇️ Download Script",
            st.session_state["script"],
            file_name="video_script.txt"
        )

        st.markdown('</div>', unsafe_allow_html=True)


# ---------- RUN ----------
if __name__ == "__main__":
    main()