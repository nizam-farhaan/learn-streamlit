"""
08 - Streaming: waiting vs streaming, side by side
==================================================
CONCEPT : st.write_stream(generator) prints each piece as it is yielded
          and RETURNS the full text at the end.
WHY     : LLMs take seconds to finish. Streaming cuts the TIME TO FIRST
          WORD, so the app FEELS fast. Total time stays the same.
RUN     : streamlit run 08_streaming.py   (no API key needed)
TRY     : Click both buttons and compare the two metrics on each side.
          Then make the "LLM" slower with the slider and try again.

ANALOGY : A waiter who brings each dish when ready vs one who waits until
          the whole table's order is cooked.
"""

import time

import streamlit as st

st.set_page_config(page_title="Streaming", page_icon="🌊", layout="wide")
st.title("🌊 Streaming: same total time, very different feel")

ANSWER = ("Streamlit reruns your script on every interaction. session_state "
          "keeps memory between reruns, caching avoids redoing slow work, and "
          "streaming shows each word the moment the model produces it.")

speed = st.slider("🐢 How slow is our fake LLM? (seconds per word)", 0.02, 0.2, 0.08)

if "results" not in st.session_state:
    st.session_state.results = {}


def fake_llm(text):
    """A generator: yields one word at a time, like an LLM API does."""
    for word in text.split():
        time.sleep(speed)
        yield word + " "


def timed(gen, side):
    """Wraps a generator and records when the first word arrived."""
    start = time.time()
    first = None
    for piece in gen:
        if first is None:
            first = time.time() - start
        yield piece
    st.session_state.results[side] = {"first": first, "total": time.time() - start}


def show_metrics(side):
    r = st.session_state.results.get(side)
    if r:
        m1, m2 = st.columns(2)
        m1.metric("⏱️ Time to first word", f"{r['first']:.2f} s")
        m2.metric("🏁 Total time", f"{r['total']:.2f} s")


left, right = st.columns(2, border=True)

with left:
    st.subheader("❌ Wait for the full answer")
    if st.button("▶️ Ask", key="wait"):
        start = time.time()
        with st.spinner("Thinking..."):
            full = "".join(fake_llm(ANSWER))       # collect EVERYTHING first
        total = time.time() - start
        st.session_state.results["wait"] = {"first": total, "total": total}
        st.session_state.wait_text = full
    st.write(st.session_state.get("wait_text", ""))
    show_metrics("wait")

with right:
    st.subheader("✅ Stream with st.write_stream")
    if st.button("▶️ Ask", key="stream"):
        st.session_state.stream_text = st.write_stream(timed(fake_llm(ANSWER), "stream"))
    elif "stream_text" in st.session_state:
        st.write(st.session_state.stream_text)     # redraw saved text on reruns
    show_metrics("stream")

st.divider()
c1, c2 = st.columns(2)
with c1:
    st.markdown("**🔑 Key line**")
    st.code("full_text = st.write_stream(generator)\n"
            "# shows pieces live, RETURNS the whole text -> save it!", language="python")
with c2:
    st.markdown("**⚠️ Catches**")
    st.markdown("- You can't check the output before the user sees it\n"
                "- Half a JSON is invalid JSON → don't stream structured output\n"
                "- Save the returned text, or it's gone on the next rerun")
