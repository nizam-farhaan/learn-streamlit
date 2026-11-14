"""
09 - A real AI chatbot (Gemini) - everything combined
=====================================================
CONCEPT : chat UI (07) + session_state (04) + caching (06) + streaming (08)
          + secrets (never hardcode keys) = a deployable AI app.
WHY     : This is the file you deploy. Swap `stream_reply` for YOUR backend
          (RAG, agent, anything) and you have a frontend for it.
RUN     : 1. Copy .streamlit/secrets.toml.example -> .streamlit/secrets.toml
          2. Put your Gemini key in it (free key: https://aistudio.google.com)
          3. streamlit run 09_ai_chatbot.py
TRY     : Click a suggestion, then ask a follow-up like "explain that simpler".
          Open "What we sent to Gemini" - the WHOLE history goes every time.
          Switch persona and ask the same question again.
"""

import time

import streamlit as st
from google import genai

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

MODEL = "gemini-3.5-flash-lite"   # change in ONE place if Google renames it
PERSONAS = {
    "🎓 Friendly tutor": "You are a friendly tutor. Keep answers short and clear.",
    "💼 Interview coach": "You are a strict but kind interview coach. Answer, then "
                         "ask one follow-up question to test understanding.",
    "🧒 Explain like I'm 5": "Explain everything like the user is 5 years old, "
                            "using simple words and one everyday analogy.",
}
SUGGESTIONS = ["What is RAG?", "Explain embeddings simply", "What does an AI engineer do?"]


# ---- 1. API key: secrets first, sidebar input as fallback ---------------
def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]        # local file or cloud secret
    except Exception:
        return st.sidebar.text_input("🔑 Gemini API key", type="password")


# ---- 2. Cache the client: create it once, not on every message ----------
@st.cache_resource
def get_client(api_key: str):
    return genai.Client(api_key=api_key)


# ---- 3. The "brain": swap this for your RAG / agent backend -------------
def to_gemini(messages):
    # Gemini uses role "model" where we use "assistant"
    return [{"role": "model" if m["role"] == "assistant" else "user",
             "parts": [{"text": m["content"]}]} for m in messages]


def stream_reply(client, messages, system_prompt, temperature):
    stream = client.models.generate_content_stream(
        model=MODEL,
        contents=to_gemini(messages),
        config={"system_instruction": system_prompt, "temperature": temperature},
    )
    for chunk in stream:
        if chunk.text:
            yield chunk.text


def timed(gen):
    """Records time to first token and total time for the sidebar."""
    start, first = time.time(), None
    for piece in gen:
        if first is None:
            first = time.time() - start
        yield piece
    st.session_state.last_speed = (first or 0, time.time() - start)


# ---- 4. Sidebar: settings + live stats ----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("⚙️ Settings")
    persona = st.selectbox("Persona", list(PERSONAS))
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.4)
    st.caption(f"Model: `{MODEL}`")
    if st.button("🗑️ New chat"):
        st.session_state.messages = []
        st.session_state.pop("last_speed", None)

    st.header("📊 Stats")
    s1, s2 = st.columns(2)
    s1.metric("Messages", len(st.session_state.messages))
    if "last_speed" in st.session_state:
        first, total = st.session_state.last_speed
        s2.metric("1st token", f"{first:.2f} s")
        st.metric("Last reply total", f"{total:.2f} s")

api_key = get_api_key()

st.title("🤖 My AI Chatbot")
st.caption(f"{persona} · powered by Gemini")

if not api_key:
    st.info("👈 Add your Gemini API key in the sidebar (or in secrets.toml) to start.")
    st.stop()                                   # stop the script here

client = get_client(api_key)

# ---- 5. Chat ------------------------------------------------------------
AVATARS = {"user": "🧑‍🎓", "assistant": "🤖"}

for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar=AVATARS[m["role"]]):
        st.markdown(m["content"])

# Empty chat: show clickable suggestions
clicked = None
if not st.session_state.messages:
    st.markdown("**Try one of these:**")
    cols = st.columns(len(SUGGESTIONS))
    for col, text in zip(cols, SUGGESTIONS):
        if col.button(text, width="stretch"):
            clicked = text

prompt = st.chat_input("Ask me anything") or clicked
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=AVATARS["user"]):
        st.markdown(prompt)

    failed = False
    with st.chat_message("assistant", avatar=AVATARS["assistant"]):
        try:
            answer = st.write_stream(timed(stream_reply(
                client, st.session_state.messages, PERSONAS[persona], temperature)))
        except Exception as e:                  # bad key, quota, network...
            failed = True
            answer = "Sorry, something went wrong. Please try again."
            st.error(f"{answer}\n\nDetails: {e}")

    # Save the FULL answer, or it vanishes on the next rerun
    st.session_state.messages.append({"role": "assistant", "content": answer})
    if not failed:
        st.rerun()                              # refresh sidebar stats

# ---- 6. Glass box: exactly what goes to the model -----------------------
if st.session_state.messages:
    with st.expander("🔍 What we sent to Gemini (the whole history, every time)"):
        st.write("**System instruction:**", PERSONAS[persona])
        st.json(to_gemini(st.session_state.messages))
