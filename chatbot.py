import streamlit as st
import google.generativeai as genai

# --- CONFIGURE API ---
genai.configure(api_key="AIzaSyA5fU4CV5mfbk5pYleH176m_tHmpLp1XQY")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- PAGE SETTINGS ---
st.set_page_config(page_title="ABRGPT", page_icon="🤖", layout="wide")
st.markdown(
    "<style>html, body, [class*='css']  { font-family: 'Segoe UI', sans-serif; }</style>",
    unsafe_allow_html=True
)

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
        .main {
            # background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%);
        }
        .block-container {
            padding: 2rem 3rem;
        }
        .chat-bubble-user {
            background-color: #DCF8C6;
            color: black;
            padding: 0.75rem 1rem;
            border-radius: 1.5rem;
            max-width: 75%;
            margin-left: auto;
            margin-bottom: 1rem;
        }
        .chat-bubble-bot {
            background-color: #F1F0F0;
            color: black;
            padding: 0.75rem 1rem;
            border-radius: 1.5rem;
            max-width: 75%;
            margin-right: auto;
            margin-bottom: 1rem;
        }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    # st.image("https://upload.wikimedia.org/wikipedia/commons/5/5e/Google_Gemini_logo.svg", width=200)
    st.image("cabr.png", width=350)
    st.markdown("### 🤖 ABRGPT")
    st.markdown("Ask anything & get instant responses from 'ABRGPT AI'.")
    if st.button("🧹 New Chat"):
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()

    if "chat" in st.session_state:
        history_text = "\n".join(
            f"{msg.role}: {msg.parts[0].text}" for msg in st.session_state.chat.history
        )
        st.download_button("💾 Download Chat", history_text, file_name="gemini_chat.txt")

# --- INIT CHAT ---
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

st.markdown("<h2 style='text-align: center;'>🤖 ABRGPT Chat Assistant</h2>", unsafe_allow_html=True)

# --- CHAT DISPLAY ---
for msg in st.session_state.chat.history:
    bubble_class = "chat-bubble-user" if msg.role == "user" else "chat-bubble-bot"
    st.markdown(f"<div class='{bubble_class}'>{msg.parts[0].text}</div>", unsafe_allow_html=True)

# --- USER INPUT ---
prompt = st.chat_input("Type your message...")

if prompt:
    st.markdown(f"<div class='chat-bubble-user'>{prompt}</div>", unsafe_allow_html=True)

    with st.spinner("Gemini is thinking..."):
        response = st.session_state.chat.send_message(prompt)
        st.markdown(f"<div class='chat-bubble-bot'>{response.text}</div>", unsafe_allow_html=True)
