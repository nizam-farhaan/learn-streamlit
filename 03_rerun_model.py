"""
03 - The rerun model (THE most important idea)
==============================================
CONCEPT : On EVERY interaction (click, type, slide) Streamlit runs your
          whole script again, from line 1 to the last line.
WHY     : This explains almost every "weird" Streamlit bug.
RUN     : streamlit run 03_rerun_model.py
TRY     : Click "Add 1" five times. Watch the RUN LOG: the run number keeps
          growing, but the `count` variable is 1 every single time.
NOTE    : The counter is broken ON PURPOSE. 04_session_state.py fixes it.

ANALOGY : A whiteboard that is wiped after every click. The teacher redraws
          everything from their notes (your script). Anything not in the
          notes is gone.
"""

from datetime import datetime

import streamlit as st

st.set_page_config(page_title="Rerun model", page_icon="🔁", layout="wide")
st.title("🔁 The rerun model")
st.caption("This counter is broken ON PURPOSE. Let's find out why.")

# 🕵️ Spy camera: records every run of this script. It uses session_state,
# which you'll learn in 04 - for now, just trust that it remembers.
if "runs" not in st.session_state:
    st.session_state.runs = []

# ---- THE BUGGY COUNTER ---------------------------------------------------
count = 0                          # <-- runs again on EVERY click -> back to 0

clicked = st.button("➕ Add 1", type="primary")
if clicked:
    count += 1                     # 0 + 1 = 1 ... every single time

# ---- Record this run -----------------------------------------------------
st.session_state.runs.append({
    "Run #": len(st.session_state.runs) + 1,
    "Time": datetime.now().strftime("%H:%M:%S.%f")[:-3],
    "What triggered it": "➕ Add 1 click" if clicked else "page load / other",
    "count = ": count,
})

c1, c2 = st.columns(2, border=True)
c1.metric("Counter (buggy)", count)
c2.metric("Times the script has run", len(st.session_state.runs))

# ---- The run log ---------------------------------------------------------
st.subheader("🕵️ Run log (newest first)")
st.dataframe(st.session_state.runs[::-1], hide_index=True, width="stretch")

with st.container(border=True):
    st.markdown(
        "**What happens on each click**\n\n"
        "1. 🖱️ You click **Add 1**\n"
        "2. 🔁 Streamlit runs the file again from line 1\n"
        "3. 🧹 `count = 0` runs again, so the old value is wiped\n"
        "4. ➕ `count += 1` makes it **1**\n"
        "5. 🖥️ The page is redrawn showing **1**, every time\n\n"
        "**Fix:** keep the value somewhere that survives reruns → `04_session_state.py`"
    )

if st.button("🧹 Clear run log"):
    st.session_state.runs = []
    st.rerun()
