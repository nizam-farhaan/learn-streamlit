"""
05 - Layout: build a mini dashboard
===================================
CONCEPT : Containers decide WHERE things appear: sidebar, columns, tabs,
          expander, and st.empty (a placeholder you fill later).
WHY     : Real apps keep settings in a sidebar and results in the main area.
RUN     : streamlit run 05_layout.py
TRY     : Change the sidebar filters and watch every section update.
          Click "Start cooking" to see a placeholder being replaced.
"""

import time

import streamlit as st

st.set_page_config(page_title="Layout", page_icon="📐", layout="wide")

MENU = [
    {"Dish": "Biryani",        "Type": "Non-veg", "Price": 250, "Rating": 4.7, "Spice": 3},
    {"Dish": "Paneer Tikka",   "Type": "Veg",     "Price": 220, "Rating": 4.5, "Spice": 2},
    {"Dish": "Masala Dosa",    "Type": "Veg",     "Price": 90,  "Rating": 4.6, "Spice": 1},
    {"Dish": "Butter Chicken", "Type": "Non-veg", "Price": 280, "Rating": 4.8, "Spice": 2},
    {"Dish": "Chole Bhature",  "Type": "Veg",     "Price": 140, "Rating": 4.3, "Spice": 3},
    {"Dish": "Fish Curry",     "Type": "Non-veg", "Price": 300, "Rating": 4.4, "Spice": 4},
    {"Dish": "Idli Sambar",    "Type": "Veg",     "Price": 70,  "Rating": 4.2, "Spice": 1},
]

# ---- SIDEBAR: settings live here -----------------------------------------
with st.sidebar:
    st.header("⚙️ Filters")
    veg_only = st.toggle("🥦 Veg only")
    max_price = st.slider("Max price (₹)", 50, 300, 300, step=10)
    sort_by = st.selectbox("Sort by", ["Rating", "Price"])
    st.caption("📐 This whole panel is `with st.sidebar:`")

dishes = [d for d in MENU
          if d["Price"] <= max_price and (not veg_only or d["Type"] == "Veg")]
dishes.sort(key=lambda d: d[sort_by], reverse=(sort_by == "Rating"))

st.title("📐 Layout: a mini restaurant dashboard")

if not dishes:
    st.warning("No dishes match these filters. Loosen them in the sidebar.")
    st.stop()

# ---- COLUMNS: metrics side by side ---------------------------------------
c1, c2, c3, c4 = st.columns(4, border=True)
c1.metric("Dishes", len(dishes))
c2.metric("Avg price", f"₹{sum(d['Price'] for d in dishes) / len(dishes):.0f}")
c3.metric("Top rated", max(dishes, key=lambda d: d["Rating"])["Dish"])
c4.metric("Cheapest", min(dishes, key=lambda d: d["Price"])["Dish"])
st.caption("📐 Above: `st.columns(4)`, one metric per column")

# ---- TABS: different views of the same data ------------------------------
tab_menu, tab_chart, tab_raw = st.tabs(["📋 Menu", "📊 Price chart", "🧾 Raw data"])
with tab_menu:
    st.dataframe(dishes, hide_index=True, width="stretch")
with tab_chart:
    st.bar_chart(dishes, x="Dish", y="Price", height=300)
with tab_raw:
    st.json(dishes)
st.caption("📐 Above: `st.tabs([...])`, three views of the same filtered list")

# ---- PLACEHOLDER: reserve a spot, fill it later --------------------------
st.subheader("👨‍🍳 Kitchen status")
spot = st.empty()                     # reserved spot
spot.info("Kitchen idle. Click the button.")
if st.button("🔥 Start cooking", type="primary"):
    for pct in range(0, 101, 5):
        spot.progress(pct, text=f"Cooking... {pct}%")   # same spot, replaced
        time.sleep(0.05)
    spot.success("✅ Order ready!")
st.caption("📐 Above: `st.empty()`, one spot replaced again and again (info → progress → success)")

# ---- EXPANDER: hide details until needed ---------------------------------
with st.expander("🧱 How this page is built"):
    st.code(
        "with st.sidebar:           # filters\n"
        "c1, c2, c3, c4 = st.columns(4)   # metrics row\n"
        "tab1, tab2, tab3 = st.tabs([...]) # menu / chart / raw\n"
        "spot = st.empty()          # kitchen status placeholder\n"
        "with st.expander(...):     # this box",
        language="python",
    )
