import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tavily import TavilyClient

# ---------- SETUP ----------
load_dotenv()

tavily_client = TavilyClient()

# Default models
GROQ_MODELS = {
    "Llama 3 (Fast)": "llama-3.3-70b-versatile",
    "OpenAI (Balanced)": "openai/gpt-oss-120b",
    "Qwen (Efficient)": "qwen/qwen3-32b"
}

st.set_page_config(
    page_title="VidAgent AI | Viral Script Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">

<style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at top right, #2d1b4e, #1a1a2e, #0f172a);
        color: #f8fafc;
        font-family: 'Outfit', sans-serif;
    }

    /* Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Typography */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #c084fc, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 1px;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 12px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        border: none !important;
    }
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #8b5cf6, #6366f1) !important;
        color: white !important;
    }
    .stButton>button[kind="primary"]:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.4) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Input Fields */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 12px 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------- FUNCTIONS ----------
def get_realtime_info(query, model_name):
    try:
        response = tavily_client.search(query=query, max_results=3)

        if response and response.get("results"):
            summaries = []
            for r in response["results"]:
                title = r.get("title", "")
                snippet = r.get("snippet", "")
                url = r.get("url", "")
                summaries.append(f"Title: {title}\nSnippet: {snippet}\nURL: {url}")

            source_info = "\n\n---\n\n".join(summaries)
        else:
            source_info = f"No recent updates found for {query}"

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

    prompt = f"""
    You are an elite researcher. Analyze the following real-time data and create a 200-word executive summary about: "{query}".
    
    Structure it with:
    1. Key Facts
    2. Recent Developments
    3. Why it matters now
    
    Data:
    {source_info}
    """

    try:
        model = ChatGroq(model=model_name)
        response = model.invoke(prompt)
        return response.content
    except Exception as e:
        st.error(f"AI Generation Error: {e}")
        return source_info


def generate_video_script(info_text, model_name, tone, target_length):
    length_desc = "short and punchy (60 seconds)" if target_length == "Short" else "detailed and explanatory (2-3 minutes)"
    
    prompt = f"""
    Create a high-retention social media video script based on the summary below.
    
    Tone: {tone}
    Target Length: {length_desc}
    
    Guidelines:
    - [HOOK]: Start with a visual or verbal hook that stops the scroll.
    - [BODY]: Break down the core value in fast-paced segments.
    - [CTA]: End with a strong call-to-action (Subscribe/Comment).
    
    Content Summary:
    {info_text}
    """

    try:
        model = ChatGroq(model=model_name)
        response = model.invoke(prompt)
        return response.content
    except Exception as e:
        st.error(f"Script Generation Error: {e}")
        return None


# ---------- UI ----------
def main():
    # --- Sidebar ---
    with st.sidebar:
        st.image("logo.png", width=120)
        st.title("Settings")
        st.divider()
        
        selected_model_name = st.selectbox("🧠 Brain (AI Model)", list(GROQ_MODELS.keys()))
        model_id = GROQ_MODELS[selected_model_name]
        
        st.subheader("Script Preferences")
        script_tone = st.select_slider("🎭 Tone", options=["Informative", "Viral/Hype", "Professional", "Funny"])
        script_length = st.radio("⏳ Estimated Length", ["Short", "Medium"])
        
        st.divider()
        st.info("VidAgent AI uses real-time search and Groq's LPU for instant generation.")

    # --- Main Hero ---
    st.markdown('<div class="hero-title">VidAgent AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Transform Real-Time Insights into High-Retention Video Scripts</div>', unsafe_allow_html=True)

    # --- Search Section ---
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        query = st.text_input(
            "",
            placeholder="🔎 What's trending? (e.g., SpaceX Starship launch, AI developments...)",
            label_visibility="collapsed"
        )
        
        generate_btn = st.button("🚀 Research & Generate Insights", use_container_width=True, type="primary")

    if generate_btn:
        if not query:
            st.toast("⚠️ Please enter a topic first!", icon="❌")
        else:
            with st.status("🛠️ Working on it...", expanded=True) as status:
                st.write("🔍 Searching for real-time info...")
                info_result = get_realtime_info(query, model_id)
                
                if info_result:
                    st.session_state["info_result"] = info_result
                    st.session_state.pop("script", None)
                    status.update(label="✅ Insights Generated!", state="complete", expanded=False)
                else:
                    status.update(label="❌ Search Failed", state="error")

    # --- Results Display ---
    if "info_result" in st.session_state:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📊 Research & Analysis")
        st.markdown(st.session_state["info_result"])
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Script Generation ---
        if st.button("🎬 Craft Video Script", use_container_width=True):
            with st.status("✍️ Writing your viral script...", expanded=True) as status:
                script = generate_video_script(st.session_state["info_result"], model_id, script_tone, script_length)
                
                if script:
                    st.session_state["script"] = script
                    status.update(label="✅ Script Ready!", state="complete", expanded=False)
                else:
                    status.update(label="❌ Scripting Failed", state="error")

    # --- Final Script ---
    if "script" in st.session_state:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🎥 Your Viral Script")
        st.markdown(st.session_state["script"])
        
        col_dl, col_share = st.columns([1, 1])
        with col_dl:
            st.download_button(
                "⬇️ Download Text",
                st.session_state["script"],
                file_name="vidagent_script.txt",
                use_container_width=True
            )
        st.markdown('</div>', unsafe_allow_html=True)


# ---------- RUN ----------
if __name__ == "__main__":
    main()