"""
06 - Caching: stop redoing slow work on every rerun
===================================================
CONCEPT : Because the script reruns on every click, slow work (loading a
          model, connecting to a DB) would ALSO rerun every time.
          Caching runs it once and reuses the result.
WHY     : Without caching, an AI app reloads its model on every message.
RUN     : streamlit run 06_caching.py
TRY     : Tab 1 - click "Place order" 5 times on EACH side. Compare the
          spinner, the "tandoor lit" count and the bar chart.
          Tab 2 - switch cities back and forth.
          Tab 3 - open the app in TWO browser tabs and add an order in each.

ANALOGY : A restaurant lights the tandoor ONCE in the morning, not for every
          order. Lighting = slow (load model). Cooking = fast (answer).

TWO DECORATORS (memory trick: resource = tools, data = ingredients)
  @st.cache_resource -> things you LOAD/CONNECT once: ML models, DB clients,
                        LLM clients. Same object shared by ALL users.
  @st.cache_data     -> data/results: CSVs, JSON, API responses.
                        Cached per argument; each caller gets a COPY.
"""

import random
import time

import streamlit as st

st.set_page_config(page_title="Caching", page_icon="🔥", layout="wide")
st.title("🔥 Caching: light the tandoor once")

# Per-user scoreboard (session_state, NOT cache - it belongs to this user)
if "log" not in st.session_state:
    st.session_state.log = {"no_cache": [], "cache": []}
    st.session_state.lit = {"no_cache": 0, "cache": 0}


# ---- The slow job, two versions ------------------------------------------
def light_tandoor():
    """NOT cached: the body runs on every call."""
    st.session_state.lit["no_cache"] += 1    # count real executions
    time.sleep(random.uniform(1.5, 3.0))     # pretend: load a model (1.5-3 s)
    return "🔥 tandoor ready"


@st.cache_resource(show_spinner="🔥 Lighting the tandoor (first time only)...")
def light_tandoor_cached():
    """Cached: the body runs ONCE, then the stored result is returned."""
    st.session_state.lit["cache"] += 1       # only increases on a cache MISS
    time.sleep(random.uniform(1.5, 3.0))     # same slow job
    return "🔥 tandoor ready"


def place_order(side, get_tandoor):
    start = time.time()
    get_tandoor()                            # slow only if body actually runs
    wait = round(time.time() - start, 2)
    st.session_state.log[side].append(wait)


def scoreboard(side):
    waits = st.session_state.log[side]
    c1, c2, c3 = st.columns(3)
    c1.metric("Orders", len(waits))
    c2.metric("Tandoor lit", st.session_state.lit[side])
    c3.metric("Total wait", f"{sum(waits):.1f} s")
    if waits:
        st.bar_chart({"Wait per order (s)": waits}, height=220)


tab1, tab2, tab3 = st.tabs(
    ["1️⃣ cache_resource: the race", "2️⃣ cache_data: keyed by input",
     "3️⃣ ⚠️ Shared by ALL users"]
)

# ---- TAB 1: side-by-side race --------------------------------------------
with tab1:
    st.caption("Same slow job (1.5-3 s, random) on both sides. Click each button 5 times.")
    left, right = st.columns(2, border=True)

    with left:
        st.subheader("❌ Without cache")
        if st.button("Place order 🍗", key="order_no_cache"):
            with st.spinner("🔥 Lighting the tandoor AGAIN..."):
                place_order("no_cache", light_tandoor)
        scoreboard("no_cache")

    with right:
        st.subheader("✅ With @st.cache_resource")
        if st.button("Place order 🍗", key="order_cache"):
            place_order("cache", light_tandoor_cached)
        scoreboard("cache")

    if st.button("🧹 Clear cache and scores"):
        st.cache_resource.clear()            # next cached call is slow again
        st.session_state.log = {"no_cache": [], "cache": []}
        st.session_state.lit = {"no_cache": 0, "cache": 0}
        st.rerun()

# ---- TAB 2: cache_data is keyed by the arguments -------------------------
@st.cache_data(show_spinner="📂 Reading the menu file...")
def load_menu(city: str):
    time.sleep(random.uniform(0.8, 1.5))     # pretend: read a big file / API
    return [f"{city} Biryani", f"{city} Dosa", f"{city} Chai"]


with tab2:
    st.caption("Key = function + arguments. New city -> slow once. "
               "Same city again -> instant.")
    city = st.radio("City", ["Hyderabad", "Bengaluru", "Chennai"], horizontal=True)
    start = time.time()
    menu = load_menu(city)
    took = time.time() - start
    if took > 0.5:
        st.error(f"Cache MISS: read '{city}' from disk in {took:.2f} s")
    else:
        st.success(f"Cache HIT: '{city}' served from memory in {took:.3f} s")
    menu.append("🍕 Pizza (added to OUR copy)")   # change the returned list
    st.write(menu)
    st.caption("We append Pizza on every run, yet it appears only ONCE: each "
               "call gets a fresh copy, so the cached original stays clean. "
               "With cache_resource the same list would be returned and "
               "Pizza would pile up.")

# ---- TAB 3: why per-user data must NEVER be cached -----------------------
@st.cache_resource
def shared_orders():
    return []                                # ONE list for the whole server


with tab3:
    st.caption("Open this app in a SECOND browser tab and add an order there too.")
    name = st.text_input("Your name", "Student A")
    if st.button("Add my order to the cached list"):
        shared_orders().append(f"{name}: Paneer Tikka")
    st.write("Orders in the cached list:", shared_orders())
    st.error("Every user sees every order. That's how chats or personal data "
             "leak. Per-user data -> st.session_state, never cache_resource.")
    if st.button("Empty the shared list"):
        shared_orders().clear()
        st.rerun()
