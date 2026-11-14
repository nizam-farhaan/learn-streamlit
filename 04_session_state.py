"""
04 - session_state: memory that survives reruns
===============================================
CONCEPT : st.session_state is a dict-like object, ONE per browser tab,
          kept on the server. It survives reruns, but NOT a page refresh.
WHY     : Chat history, user choices, a multi-step form - all need memory.
RUN     : streamlit run 04_session_state.py
TRY     : 1. Click both "Add 1" buttons a few times and compare.
          2. Type in the inputs - watch them appear in the locker.
          3. Open the app in a second tab - it has its own locker.
          4. Refresh (F5) - the locker is emptied.

ANALOGY : A gym locker. Each visitor (tab) gets their own. Stuff stays
          between workouts (reruns). Leave the gym (refresh) -> emptied.
"""

import streamlit as st

st.set_page_config(page_title="session_state", page_icon="🗄️", layout="wide")
st.title("🗄️ session_state: memory that survives reruns")

# ---- 1. Plain variable vs session_state, side by side --------------------
left, right = st.columns(2, border=True)

with left:
    st.subheader("❌ Plain variable")
    st.code("count = 0\nif clicked:\n    count += 1", language="python")
    count = 0                                  # wiped on every rerun
    if st.button("Add 1", key="plain_btn"):
        count += 1
    st.metric("count", count)
    st.caption("Stuck at 1: `count = 0` runs on every rerun.")

with right:
    st.subheader("✅ st.session_state")
    st.code('if "count" not in st.session_state:\n    st.session_state.count = 0  # ONCE\n'
            "if clicked:\n    st.session_state.count += 1", language="python")
    if "count" not in st.session_state:        # runs only on the first run
        st.session_state.count = 0
    if st.button("Add 1", key="state_btn"):
        st.session_state.count += 1
    st.metric("st.session_state.count", st.session_state.count)
    st.caption("Keeps counting: the value lives in the locker, not in the script.")

# ---- 2. Callbacks: run code BEFORE the rerun -----------------------------
def reset_counter():
    st.session_state.count = 0

st.button("🔄 Reset (uses on_click callback)", on_click=reset_counter)

st.divider()

# ---- 3. Widgets with key= live in the locker automatically ---------------
a, b = st.columns(2, border=True)
with a:
    st.subheader("🔑 Widgets with key=")
    st.text_input("Nickname", key="nickname")
    st.selectbox("Favourite dish", ["Biryani", "Dosa", "Paneer Tikka"], key="fav_dish")
    st.write(f"Hi **{st.session_state.nickname or 'stranger'}**, "
             f"one {st.session_state.fav_dish} coming up! 🍽️")
    st.caption("We read the values from st.session_state, not from variables.")

with b:
    st.subheader("🗄️ Your locker, live")
    st.json(dict(st.session_state))
    st.caption("Everything stored for THIS tab. Widgets with key= appear here too.")

# ---- 4. Lifetime experiments ---------------------------------------------
with st.expander("🧪 Experiments: what keeps it, what wipes it"):
    st.markdown(
        "| Action | Locker |\n|---|---|\n"
        "| Click / type (rerun) | ✅ Kept |\n"
        "| Open the app in a new tab | 🆕 New, empty locker |\n"
        "| Refresh the page (F5) | 🧹 Emptied |\n"
        "| Server restarts | 🧹 Emptied |"
    )
    st.code('st.session_state["count"]      # dict style\n'
            "st.session_state.count         # attribute style (same)\n"
            'st.session_state.get("x", 0)   # safe read with default', language="python")
