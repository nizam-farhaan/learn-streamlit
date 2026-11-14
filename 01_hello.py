"""
01 - Hello Streamlit: code -> result
====================================
CONCEPT : A Streamlit app is just a Python script. Each st.* line draws
          something on the page, top to bottom, in the order you write it.
WHY     : You can build a web page without HTML, CSS or JavaScript.
RUN     : streamlit run 01_hello.py
TRY     : Every card shows the code on the LEFT and what it draws on the
          RIGHT. Edit a snippet in EXAMPLES, save, and click "Rerun"
          (top-right) to see Streamlit pick up your change.
"""

import streamlit as st

st.set_page_config(page_title="Hello Streamlit", page_icon="👋", layout="wide")

st.title("👋 Hello, Streamlit")
st.caption("Left: the Python you write.  Right: the web page you get. No HTML anywhere.")

# Each example = (what it is, the exact code). We run the code on the right.
EXAMPLES = [
    ("Title and headers",
     'st.title("🍛 My Kitchen")\nst.header("Today\'s specials")\nst.subheader("Fresh from the tandoor")'),
    ("st.write shows almost anything",
     'st.write("Plain text works.")\nst.write({"dish": "Biryani", "price": 250, "veg": False})'),
    ("Markdown for formatting",
     'st.markdown("**Bold**, *italic*, `code` and a [link](https://streamlit.io)")'),
    ("Metrics: big numbers with a change",
     'st.metric("Orders today", 128, delta="+12 vs yesterday")'),
    ("Status boxes: talk to your users",
     'st.success("Order placed!")\nst.info("Kitchen is busy, ~20 min")\n'
     'st.warning("Low stock: paneer")\nst.error("Payment failed")'),
    ("Tables from plain Python lists",
     'st.dataframe([\n    {"dish": "Biryani", "price": 250},\n    {"dish": "Dosa", "price": 90},\n'
     '], hide_index=True)'),
]

for title, code in EXAMPLES:
    with st.container(border=True):
        left, right = st.columns(2)
        with left:
            st.caption(f"✍️ {title}")
            st.code(code, language="python")
        with right:
            st.caption("🖥️ Result")
            exec(code, {"st": st})          # run the snippet inside this column

st.divider()
if st.button("🎉 I built my first web app!", type="primary"):
    st.balloons()
