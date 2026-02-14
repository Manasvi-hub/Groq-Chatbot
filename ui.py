import streamlit as st
from backend import get_response

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# -------------------- Sidebar (settings + theme) --------------------
with st.sidebar:
    st.header("Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.01, help="Higher temperature = more creative responses")
    chunk_size = st.number_input("Chunk size", min_value=128, max_value=4000, value=500, step=64, help="Document chunk size (not used yet)")
    chunk_overlap = st.number_input("Chunk overlap", min_value=0, max_value=1024, value=50, step=1, help="Overlap between chunks (not used yet)")
    max_tokens = st.number_input("Max tokens", min_value=64, max_value=8192, value=1024, step=64, help="Maximum tokens to request from the model")
    st.markdown("---")
    theme = st.radio("Theme", ["☀️ Light", "🌙 Dark"], index=0)
    if st.button("Clear chat"):
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful AI assistant"}
        ]

# -------------------- Theme CSS --------------------
base_css = """
:root{
  --bg1: #f6f8fb;
  --bg2: #e9eef6;
  --card: #ffffff;
  --text: #0f172a;
  --muted: #475569;
  --accent: linear-gradient(90deg,#7c3aed,#06b6d4);
}
.app-header{font-family: 'Helvetica Neue', Arial; font-weight:700; font-size:28px}
.chat-bubble-user{background:linear-gradient(90deg,#bde4ff, #d4f1ff); padding:12px; border-radius:14px; color:var(--text)}
.chat-bubble-assistant{background:var(--card); padding:12px; border-radius:14px; color:var(--text); border:1px solid rgba(15,23,42,0.06)}
.meta{color:var(--muted); font-size:12px}
.app-bg{background: radial-gradient(circle at 10% 10%, rgba(124,58,237,0.06), transparent 10%), radial-gradient(circle at 90% 90%, rgba(6,182,212,0.04), transparent 10%); padding:24px; border-radius:12px}
"""

dark_overrides = """
:root{ --bg1:#000000; --bg2:#000000; --card:#0b0b0b; --text:#e6eef8; --muted:#94a3b8 }
html, body, .stApp, .block-container, .main, .css-1outpf7, .css-18e3th9 {background:#000000 !important; color: #e6eef8 !important; height:100%}
.stApp, .main, .block-container {min-height:100vh; max-width:100vw; padding:24px 48px !important; margin:0 auto}
.stApp > .main > .block-container {padding-top:24px}
.stSidebar, .sidebar-content, .css-1lcbmhc {background:#000000 !important; color: #e6eef8 !important}
.app-bg{background: none}
.chat-bubble-user{background: linear-gradient(90deg,#0b1115,#071018); color:var(--text); text-shadow: 0 0 8px rgba(230,238,248,0.12)}
.chat-bubble-assistant{background: #0b0b0b; color:var(--text); border:1px solid rgba(255,255,255,0.04); text-shadow: 0 0 6px rgba(230,238,248,0.10)}
.app-header{color:var(--text)!important; text-shadow: 0 0 18px rgba(124,58,237,0.40), 0 0 8px rgba(6,182,212,0.25)}
.meta{color:var(--muted)!important}
/* make inputs/buttons dark */
input, textarea, button, .stButton>button, .stTextInput>div>input {background:#0b0b0b !important; color:#e6eef8 !important; border:1px solid rgba(255,255,255,0.04) !important}
/* subtle glow for important text */
.glow { text-shadow: 0 0 10px rgba(230,238,248,0.9), 0 0 18px rgba(124,58,237,0.12); }
/* full-bleed fixed background layer to ensure entire screen is black */
.section-full {position:fixed; inset:0; z-index:-1; background:#000}
"""

is_dark = ("Dark" in theme) or theme.strip().startswith("🌙")
css = base_css + (dark_overrides if is_dark else "")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
if is_dark:
    st.markdown("<div class='section-full'></div>", unsafe_allow_html=True)

# -------------------- Main UI --------------------
st.markdown("<div class='app-header' style='background: -webkit-linear-gradient(#7c3aed,#06b6d4); -webkit-background-clip: text; color: transparent;'>🤖 Groq Chatbot</div>", unsafe_allow_html=True)
st.markdown("<div class='meta'>Beautiful, minimal chat interface — tweak settings in the sidebar.</div>", unsafe_allow_html=True)
st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# session memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful AI assistant"}
    ]

cols = st.columns([3, 1])
with cols[0]:
    # show chat history
    for msg in st.session_state.messages[1:]:
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
        if role == "user":
            st.markdown(f"<div class='chat-bubble-user'>{content}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble-assistant'>{content}</div>", unsafe_allow_html=True)

with cols[1]:
    # quick settings summary
    st.markdown("**Current settings**")
    st.write(f"Temperature: {temperature}")
    st.write(f"Max tokens: {max_tokens}")
    st.write(f"Chunk size: {chunk_size}")
    st.write(f"Chunk overlap: {chunk_overlap}")
    st.write(f"Theme: {theme}")

# input
prompt = st.chat_input("Type message...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Thinking..."):
        reply = get_response(
            st.session_state.messages,
            temperature=float(temperature),
            max_tokens=int(max_tokens),
            chunk_size=int(chunk_size),
            chunk_overlap=int(chunk_overlap),
        )
    st.session_state.messages.append({"role": "assistant", "content": reply})