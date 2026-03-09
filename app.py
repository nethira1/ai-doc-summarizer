import streamlit as st
from groq import Groq
import fitz  # PyMuPDF

st.set_page_config(page_title="AI Document Summarizer", page_icon="📄", layout="centered")

st.markdown("""
<style>
    .stButton>button { background-color: #4F46E5; color: white; border-radius: 8px; padding: 0.5rem 2rem; font-weight: 600; border: none; }
    .result-box { background: #F8FAFC; border-left: 4px solid #4F46E5; padding: 1rem 1.5rem; border-radius: 0 8px 8px 0; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

st.title("📄 AI Document Summarizer")
st.markdown("Upload a **PDF or text file** and get an instant AI-powered summary!")
st.divider()

with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    st.markdown("[🔑 Get FREE API key →](https://console.groq.com)")
    st.divider()
    st.markdown("**✅ Groq Free Tier:**\n- No credit card needed!\n- Works in India 🇮🇳\n- Super fast responses!")
    st.divider()
    st.markdown("**How to use:**\n1. Get free Groq API key\n2. Paste key above\n3. Upload document\n4. Click Summarize!")

def extract_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    return "".join(page.get_text() for page in doc).strip()

def extract_text_from_txt(file_bytes):
    return file_bytes.decode("utf-8", errors="ignore").strip()

def call_groq(api_key, prompt):
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )
    return response.choices[0].message.content

for key in ["doc_text", "summary", "key_points"]:
    if key not in st.session_state:
        st.session_state[key] = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("📁 Upload your document", type=["pdf", "txt"])

if uploaded_file:
    file_bytes = uploaded_file.read()
    if uploaded_file.type == "application/pdf":
        st.session_state.doc_text = extract_text_from_pdf(file_bytes)
    else:
        st.session_state.doc_text = extract_text_from_txt(file_bytes)
    word_count = len(st.session_state.doc_text.split())
    st.success(f"✅ Loaded: **{uploaded_file.name}** ({word_count:,} words)")
    with st.expander("👁️ Preview text"):
        st.text(st.session_state.doc_text[:2000])

if st.session_state.doc_text:
    if st.button("✨ Summarize Document"):
        if not api_key:
            st.error("⚠️ Please enter your Groq API key in the sidebar!")
        else:
            with st.spinner("🤖 AI is reading your document..."):
                try:
                    text = st.session_state.doc_text[:6000]
                    st.session_state.summary = call_groq(api_key, f"Give a clear 3-5 sentence summary of this document:\n\n{text}")
                    st.session_state.key_points = call_groq(api_key, f"List the 5 most important key points from this document as bullet points:\n\n{text}")
                    st.session_state.chat_history = []
                except Exception as e:
                    st.error(f"❌ Error: {e}")

if st.session_state.summary:
    st.divider()
    st.subheader("📝 Summary")
    st.markdown(f'<div class="result-box">{st.session_state.summary}</div>', unsafe_allow_html=True)
    st.subheader("🔑 Key Points")
    st.markdown(f'<div class="result-box">{st.session_state.key_points}</div>', unsafe_allow_html=True)
    st.divider()
    st.subheader("💬 Ask Questions")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    question = st.chat_input("Ask anything about the document...")
    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    answer = call_groq(api_key, f"Answer based ONLY on this document:\n\n{st.session_state.doc_text[:6000]}\n\nQuestion: {question}")
                    st.markdown(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Error: {e}")