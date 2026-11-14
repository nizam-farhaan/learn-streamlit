"""
07 - A chat UI (no AI yet): Parrot bot
======================================
CONCEPT : st.chat_input  -> text box pinned to the bottom; returns the text
                            or None.
          st.chat_message -> a chat bubble ("user" / "assistant").
          session_state   -> the list of messages, so history survives reruns.
WHY     : This is the skeleton of every chatbot UI. In 09 we swap the parrot
          for a real LLM.
RUN     : streamlit run 07_chat_basic.py
TRY     : Send 3 messages. Then switch ON "Simulate the bug" in the sidebar
          and send 2 more - the history vanishes. Watch the sidebar viewer.
"""

import streamlit as st

st.set_page_config(page_title="Parrot bot", page_icon="🦜")
st.title("🦜 Parrot bot")
st.caption("A chat UI with no AI: it repeats what you say. The structure is what matters.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---- SIDEBAR: bug switch + live view of the history ----------------------
with st.sidebar:
    st.header("🔬 Under the hood")
    show_bug = st.toggle("🐞 Simulate the bug (no session_state)")
    if show_bug:
        st.error("History is a plain list `messages = []`, reset on every rerun.")
        messages = []                                  # wiped on every rerun!
    else:
        st.success("History lives in `st.session_state.messages`.")
        messages = st.session_state.messages

    st.metric("Messages in history", len(messages))
    with st.expander("📦 The history list", expanded=True):
        st.json(messages)
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()

# ---- 1. Redraw the whole conversation (runs on every rerun) --------------
if not messages:
    with st.chat_message("assistant", avatar="🦜"):
        st.write("Hi! Say anything and I'll repeat it. Squawk!")

for m in messages:
    with st.chat_message(m["role"], avatar="🧑‍🎓" if m["role"] == "user" else "🦜"):
        st.write(m["content"])

# ---- 2. Handle a new message ---------------------------------------------
prompt = st.chat_input("Say something")
if prompt:                                             # None until user sends
    messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.write(prompt)

    reply = f"🦜 *{prompt}*! ({len(prompt.split())} words, squawk!)"   # the "brain"
    messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant", avatar="🦜"):
        st.write(reply)
