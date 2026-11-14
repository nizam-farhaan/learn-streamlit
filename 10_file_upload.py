"""
10 - File upload + AI: chat with a PDF in one click
===================================================
CONCEPT : st.file_uploader gives you the uploaded file as an in-memory
          object. Read it, send the text to an LLM, show the result.
WHY     : Many AI apps start with "upload your document" - resume matchers,
          PDF Q&A, invoice readers. (S19's Resume-JD Matcher uses this.)
RUN     : needs .streamlit/secrets.toml with GEMINI_API_KEY
          streamlit run 10_file_upload.py
TRY     : Upload your resume PDF, check the stats, then click "Strengths & gaps".
"""

import io

import streamlit as st
from google import genai
from pypdf import PdfReader

st.set_page_config(page_title="PDF + AI", page_icon="📄", layout="wide")

MODEL = "gemini-3.5-flash-lite"
MAX_CHARS = 20_000      # guard: don't send a 300-page book to the model
ACTIONS = {
    "📝 Summarize": "Summarize this document in 5 short bullet points.",
    "🎯 Key facts": "List the 5 most important facts or numbers in this document.",
    "💪 Strengths & gaps": "If this is a resume, list 3 strengths and 3 gaps for a "
                          "GenAI Engineer role. Otherwise, list 3 strong and 3 weak points.",
}


@st.cache_resource
def get_client(api_key: str):
    return genai.Client(api_key=api_key)


@st.cache_data          # same file -> no need to re-read it on every rerun
def pdf_to_text(file_bytes: bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text, len(reader.pages)


st.title("📄 PDF + AI")
st.caption("Upload → extract text → send to Gemini → stream the answer")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = st.sidebar.text_input("🔑 Gemini API key", type="password")

uploaded = st.file_uploader("Drop a PDF here", type=["pdf"])

if not uploaded:
    st.info("👆 Upload a PDF to begin. Your resume is a great test.")
    st.stop()

text, pages = pdf_to_text(uploaded.getvalue())
words = len(text.split())

# ---- Stats: what did we actually get from the file? ----------------------
c1, c2, c3, c4 = st.columns(4, border=True)
c1.metric("📄 Pages", pages)
c2.metric("🔤 Words", f"{words:,}")
c3.metric("🔢 Characters", f"{len(text):,}")
c4.metric("⏱️ Reading time", f"{max(1, round(words / 200))} min")

if len(text) > MAX_CHARS:
    st.warning(f"Long document: only the first {MAX_CHARS:,} characters are sent to the model.")

with st.expander("👀 What the model will read (extracted text)"):
    st.text(text[:3000] + ("..." if len(text) > 3000 else ""))

if not text.strip():
    st.error("No text found. This looks like a scanned PDF (images) - it needs OCR.")
    st.stop()
if not api_key:
    st.info("👈 Add your Gemini API key in the sidebar to run the AI actions.")
    st.stop()

# ---- One-click actions + a custom one ------------------------------------
st.subheader("⚡ What should the AI do?")
task = None
cols = st.columns(len(ACTIONS))
for col, (label, instruction) in zip(cols, ACTIONS.items()):
    if col.button(label, width="stretch"):
        task = instruction
custom = st.text_input("…or type your own instruction")
if st.button("▶️ Run custom", disabled=not custom):
    task = custom

if task:
    with st.container(border=True):
        st.caption(f"🧠 Task: {task}")
        prompt = f"{task}\n\nDocument:\n{text[:MAX_CHARS]}"
        try:
            stream = get_client(api_key).models.generate_content_stream(
                model=MODEL, contents=prompt
            )
            st.write_stream(c.text for c in stream if c.text)
        except Exception as e:
            st.error(f"Model call failed: {e}")
