"""
02 - Inputs (widgets): build an order, watch the receipt
========================================================
CONCEPT : Widgets take input from the user. Each widget call RETURNS the
          current value, so you use it like a normal Python variable.
WHY     : Every AI app needs inputs: a prompt, a model choice, a temperature.
RUN     : streamlit run 02_inputs.py
TRY     : Change any input and watch the receipt update instantly.
          You never wrote an "on change" handler. Why does it update?
          (Answer in 03_rerun_model.py)
"""

import streamlit as st

st.set_page_config(page_title="Widgets", page_icon="🧾", layout="wide")
st.title("🧾 Widgets return values")
st.caption("Left: widgets. Right: the plain Python values they return, used to build a receipt.")

PRICES = {"Biryani": 250, "Paneer Tikka": 220, "Masala Dosa": 90, "Butter Chicken": 280}
ADD_ONS = {"Raita": 30, "Gulab Jamun": 60, "Cold Drink": 40}

left, right = st.columns([3, 2], border=True)

# ---- LEFT: every widget returns a value -----------------------------------
with left:
    st.subheader("🛒 Build your order")
    name = st.text_input("Your name", "Farhaan")                    # -> str
    dish = st.selectbox("Dish", list(PRICES))                        # -> str
    qty = st.number_input("Quantity", min_value=1, max_value=10, value=1)  # -> int
    spice = st.slider("Spice level", 0, 5, 2)                        # -> int
    size = st.radio("Portion", ["Half", "Full"], horizontal=True)    # -> str
    extras = st.multiselect("Add-ons", list(ADD_ONS))                # -> list
    express = st.toggle("Express delivery (+₹50)")                   # -> bool
    clicked = st.button("Place order", type="primary")               # -> bool

# ---- RIGHT: use them like normal variables --------------------------------
with right:
    st.subheader("🧾 Live receipt")
    base = PRICES[dish] * (0.6 if size == "Half" else 1)
    total = base * qty + sum(ADD_ONS[e] for e in extras) + (50 if express else 0)

    st.write(f"**Customer:** {name or '—'}")
    st.write(f"**{qty} × {size} {dish}** — ₹{base * qty:.0f}")
    st.write(f"**Spice:** {'🌶️' * spice or 'None'}")
    for e in extras:
        st.write(f"+ {e} — ₹{ADD_ONS[e]}")
    if express:
        st.write("+ Express delivery — ₹50")
    st.metric("Total", f"₹{total:.0f}")

    if clicked:                                   # True for ONE run only
        st.success(f"Order placed, {name}! 🎉")
        st.balloons()

# ---- What Python actually received -----------------------------------------
st.subheader("🔍 What each widget returned")
st.dataframe(
    [
        {"Widget": "st.text_input", "Value": repr(name), "Python type": type(name).__name__},
        {"Widget": "st.selectbox", "Value": repr(dish), "Python type": type(dish).__name__},
        {"Widget": "st.number_input", "Value": repr(qty), "Python type": type(qty).__name__},
        {"Widget": "st.slider", "Value": repr(spice), "Python type": type(spice).__name__},
        {"Widget": "st.radio", "Value": repr(size), "Python type": type(size).__name__},
        {"Widget": "st.multiselect", "Value": repr(extras), "Python type": type(extras).__name__},
        {"Widget": "st.toggle", "Value": repr(express), "Python type": type(express).__name__},
        {"Widget": "st.button", "Value": repr(clicked), "Python type": type(clicked).__name__},
    ],
    hide_index=True,
    width="stretch",
)
st.caption("Notice st.button: True only on the run right after the click, then back to False.")
