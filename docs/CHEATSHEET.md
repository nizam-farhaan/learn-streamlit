# Streamlit Cheat Sheet

## The one rule
**Every interaction reruns the whole script, top to bottom.**
Memory → `session_state`. Slow work → cache.

## Run
```bash
pip install streamlit
streamlit run app.py
```

## Display
```python
st.title("Title"); st.header("H"); st.subheader("h")
st.write(anything)            # text, dict, list, DataFrame...
st.markdown("**bold**")
st.code("x = 1", language="python")
st.metric("Latency", "320 ms", delta="-40 ms")
st.success("ok"); st.info("i"); st.warning("w"); st.error("e")
```

## Inputs (each returns a value)
```python
txt  = st.text_input("Name")
num  = st.number_input("Age", 0, 100, 22)
temp = st.slider("Temp", 0.0, 1.0, 0.7)
opt  = st.selectbox("Model", ["a", "b"])
flag = st.checkbox("Verbose")
if st.button("Go"): ...       # True for ONE run only
f    = st.file_uploader("PDF", type=["pdf"])
```

## Layout
```python
with st.sidebar: ...
c1, c2 = st.columns(2)
t1, t2 = st.tabs(["Chat", "Debug"])
with st.expander("Details"): ...
spot = st.empty(); spot.write("replace me later")
```

## session_state (per user, survives reruns, NOT refresh)
```python
if "messages" not in st.session_state:
    st.session_state.messages = []
st.text_input("City", key="city")          # -> st.session_state.city
st.button("Reset", on_click=reset_fn)      # callback runs BEFORE rerun
```

## Caching (shared by ALL users)
```python
@st.cache_resource      # tools: models, DB clients, LLM clients
def get_client(): ...

@st.cache_data          # ingredients: CSV, JSON, API results (keyed by args)
def load(path): ...
```

## Chat + streaming
```python
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        answer = st.write_stream(my_generator(prompt))
    st.session_state.messages.append({"role": "assistant", "content": answer})
```

## Secrets
```toml
# .streamlit/secrets.toml   (in .gitignore!)
GEMINI_API_KEY = "..."
```
```python
key = st.secrets["GEMINI_API_KEY"]
```

## session_state vs cache
| | session_state | cache_resource |
|---|---|---|
| Scope | One user/tab | Whole app |
| Holds | Chat, choices | Models, clients |
| Refresh | Lost | Kept |

## Gotchas
- `python app.py` doesn't work. Use `streamlit run`.
- Forgot the `if "x" not in` check → state resets.
- Didn't save the streamed answer → reply vanishes.
- Per-user data in `cache_resource` → leaks to other users.
- Library missing from `requirements.txt` → cloud deploy fails.
