# import streamlit as st
# import google.generativeai as genai

# # --- CONFIGURE API ---
# genai.configure(api_key="AIzaSyA5fU4CV5mfbk5pYleH176m_tHmpLp1XQY")
# model = genai.GenerativeModel('gemini-1.5-flash')

# # --- PAGE SETTINGS ---
# st.set_page_config(page_title="ABRGPT", page_icon="🤖", layout="wide")
# st.markdown(
#     "<style>html, body, [class*='css']  { font-family: 'Segoe UI', sans-serif; }</style>",
#     unsafe_allow_html=True
# )

# # --- CUSTOM STYLING ---
# st.markdown("""
#     <style>
#         .main {
#             # background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%);
#         }
#         .block-container {
#             padding: 2rem 3rem;
#         }
#         .chat-bubble-user {
#             background-color: #DCF8C6;
#             color: black;
#             padding: 0.75rem 1rem;
#             border-radius: 1.5rem;
#             max-width: 75%;
#             margin-left: auto;
#             margin-bottom: 1rem;
#         }
#         .chat-bubble-bot {
#             background-color: #F1F0F0;
#             color: black;
#             padding: 0.75rem 1rem;
#             border-radius: 1.5rem;
#             max-width: 75%;
#             margin-right: auto;
#             margin-bottom: 1rem;
#         }
#         footer {visibility: hidden;}
#     </style>
# """, unsafe_allow_html=True)

# # --- SIDEBAR ---
# with st.sidebar:
#     # st.image("https://upload.wikimedia.org/wikipedia/commons/5/5e/Google_Gemini_logo.svg", width=200)
#     st.image("cabr.png", width=350)
#     st.markdown("### 🤖 ABRGPT")
#     st.markdown("Ask anything & get instant responses from 'ABRGPT AI'.")
#     if st.button("🧹 New Chat"):
#         st.session_state.chat = model.start_chat(history=[])
#         st.rerun()

#     if "chat" in st.session_state:
#         history_text = "\n".join(
#             f"{msg.role}: {msg.parts[0].text}" for msg in st.session_state.chat.history
#         )
#         st.download_button("💾 Download Chat", history_text, file_name="gemini_chat.txt")

# # --- INIT CHAT ---
# if "chat" not in st.session_state:
#     st.session_state.chat = model.start_chat(history=[])

# st.markdown("<h2 style='text-align: center;'>🤖 ABRGPT Chat Assistant</h2>", unsafe_allow_html=True)

# # --- CHAT DISPLAY ---
# for msg in st.session_state.chat.history:
#     bubble_class = "chat-bubble-user" if msg.role == "user" else "chat-bubble-bot"
#     st.markdown(f"<div class='{bubble_class}'>{msg.parts[0].text}</div>", unsafe_allow_html=True)

# # --- USER INPUT ---
# prompt = st.chat_input("Type your message...")

# if prompt:
#     st.markdown(f"<div class='chat-bubble-user'>{prompt}</div>", unsafe_allow_html=True)

#     with st.spinner("Gemini is thinking..."):
#         response = st.session_state.chat.send_message(prompt)
#         st.markdown(f"<div class='chat-bubble-bot'>{response.text}</div>", unsafe_allow_html=True)

import streamlit as st
import google.generativeai as genai
import pdfplumber  # <-- Replaces fitz
import docx
from PIL import Image  # Importing Pillow to handle images

# --- CONFIGURE API ---
genai.configure(api_key="YOUR_API_KEY")
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
        .block-container { padding: 2rem 3rem; }
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
    st.image("cabr.png", width=350)
    st.markdown("### 🤖 ABRGPT")
    st.markdown("Ask anything & get instant responses from 'ABRGPT AI'.")
    if st.button("🧹 New Chat"):
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.file_context = ""
        st.rerun()

    if "chat" in st.session_state:
        history_text = "\n".join(
            f"{msg.role}: {msg.parts[0].text}" for msg in st.session_state.chat.history
        )
        st.download_button("💾 Download Chat", history_text, file_name="gemini_chat.txt")

# --- INIT SESSION STATE ---
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "file_context" not in st.session_state:
    st.session_state.file_context = ""

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("📎 Upload a document (PDF, DOCX, TXT, or Image)", type=["pdf", "docx", "txt", "png", "jpg", "jpeg"])
if uploaded_file:
    file_text = ""
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                file_text += page.extract_text() or ""
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        file_text = "\n".join([para.text for para in doc.paragraphs])
    elif uploaded_file.type == "text/plain":
        file_text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        st.session_state.file_context = "An image has been uploaded."

    st.session_state.file_context = file_text
    st.success("✅ File uploaded and processed successfully!")
    with st.expander("📄 View Extracted File Content"):
        st.text_area("File Content", file_text, height=200)

# --- MAIN CHAT TITLE ---
st.markdown("<h2 style='text-align: center;'>🤖 ABRGPT Chat Assistant</h2>", unsafe_allow_html=True)

# --- DISPLAY CHAT HISTORY ---
for msg in st.session_state.chat.history:
    bubble_class = "chat-bubble-user" if msg.role == "user" else "chat-bubble-bot"
    st.markdown(f"<div class='{bubble_class}'>{msg.parts[0].text}</div>", unsafe_allow_html=True)

# --- USER PROMPT INPUT ---
prompt = st.chat_input("Type your message...")

if prompt:
    st.markdown(f"<div class='chat-bubble-user'>{prompt}</div>", unsafe_allow_html=True)

    # Combine file context with user prompt if file was uploaded
    full_prompt = prompt
    if st.session_state.file_context:
        full_prompt = (
            f"You are given the following document content:\n\n"
            f"{st.session_state.file_context}\n\n"
            f"Now answer this question based on the content above:\n{prompt}"
        )

    # Debugging output to check the full prompt being sent
    st.write("Full Prompt being sent:", full_prompt)  # Debugging output

    try:
        with st.spinner("Gemini is thinking..."):
            response = st.session_state.chat.send_message(full_prompt)
            st.markdown(f"<div class='chat-bubble-bot'>{response.text}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")

