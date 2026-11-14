# Learn Streamlit: Deploy Your Own AI Frontend

> You've learned to build AI **backends**: prompts, RAG, embeddings. They live in notebooks that only you can run.
> This repo teaches you to put a **frontend** on them and ship a **live link** anyone can open on their phone.

**Goal of this session:** by the end, you have a deployed AI app with a public URL in your README and resume.

---

## 1. Why are we learning this?

A recruiter sees two resumes:

| Resume A | Resume B |
|---|---|
| "Built a RAG chatbot" + GitHub link | "Built a RAG chatbot" + **live link** |
| They'd have to clone, install, add a key... they won't | They tap it and try it in 10 seconds |

**Resume B gets the call.** Your backend skills only count when someone can *use* them.

```
Your AI backend (Python)  ──►  Streamlit (frontend)  ──►  Live URL  ──►  Recruiter's phone
   prompts, RAG, agents          pure Python UI            free cloud
```

---

## 2. What is Streamlit?

**Streamlit is a Python library that turns a Python script into a web app.** No HTML, CSS or JavaScript.

```python
import streamlit as st
st.title("My first app")
name = st.text_input("Your name")
st.write("Hello", name)
```
```bash
pip install streamlit
streamlit run app.py        # NOT python app.py
```
A browser tab opens at `http://localhost:8501`. That's a web app.

**Analogy:** building a web app the usual way is like *building a house* (backend + API + frontend). Streamlit is a *furnished flat*: you walk in with your Python code and live there today. You give up design control, but you move in fast.

---

## 3. The major components

| Group | Main calls | Lesson file |
|---|---|---|
| **Display** | `st.title`, `st.write`, `st.markdown`, `st.code`, `st.metric`, `st.success/error` | `01_hello.py` |
| **Inputs (widgets)** | `st.text_input`, `st.slider`, `st.selectbox`, `st.button`, `st.file_uploader` | `02_inputs.py` |
| **Layout** | `st.sidebar`, `st.columns`, `st.tabs`, `st.expander`, `st.empty` | `05_layout.py` |
| **Memory** | `st.session_state` | `04_session_state.py` |
| **Performance** | `@st.cache_resource`, `@st.cache_data` | `06_caching.py` |
| **Chat** | `st.chat_input`, `st.chat_message` | `07_chat_basic.py` |
| **Streaming** | `st.write_stream` | `08_streaming.py` |
| **Secrets** | `st.secrets` + `.streamlit/secrets.toml` | `09_ai_chatbot.py` |

---

## 4. How Streamlit works inside (the one idea that matters)

> **Every time the user does anything (click, type, slide), Streamlit runs your whole script again, from line 1 to the last line.**

```
 User clicks a button
        │
        ▼
 Browser sends the event ──► Streamlit server
                                   │
                                   ▼
                     Re-runs app.py top to bottom
                     (widgets now return the new values)
                                   │
                                   ▼
 Browser updates only the parts ◄── New page description
 that changed
```

**Analogy:** a whiteboard wiped after every click. The teacher redraws everything from their notes (your script). Anything not in the notes is gone.

What this explains:

| Symptom | Cause | Fix |
|---|---|---|
| Counter stuck at 1 | `count = 0` runs again every rerun | `st.session_state` (`04`) |
| Chat history vanishes | `messages = []` runs again | `st.session_state` (`07`) |
| Every message takes 5 s | Model reloads every rerun | `@st.cache_resource` (`06`) |
| Button "forgets" it was clicked | `st.button` is `True` for one run only | Store the result in `session_state` |

### How does it pick up code changes?
Streamlit **watches your file**. When you save, the app shows **"Source file changed"**. Click **Rerun** or **Always rerun**, and it re-executes the new code. No server restart needed.

### Where does the state live?
- Each browser tab opens a live connection (WebSocket) to the server, which creates a **session**.
- `session_state` belongs to that session, **on the server**. It is not in the browser.
- Caches (`cache_resource`, `cache_data`) belong to the **server**, so they are **shared by all users**.

| | `session_state` | `@st.cache_resource` |
|---|---|---|
| Scope | One per user/tab | One for the whole app |
| Good for | Chat history, user choices | Models, DB clients, LLM clients |
| Survives refresh? | ❌ No | ✅ Yes (until restart) |

---

## 5. Pros and cons

| ✅ Pros | ❌ Cons |
|---|---|
| Pure Python, so a backend dev can ship a UI in an hour | Rerun model wastes work if you don't cache |
| Built-in chat, streaming, file upload | Limited design control (no pixel-perfect UI) |
| Free deploy on Streamlit Community Cloud | Not built for thousands of concurrent users |
| Perfect for demos, prototypes, internal tools | Other apps (mobile, WhatsApp) can't call it like an API |
| Huge community and examples | State is lost on refresh unless you add a DB |

**Where it fits in industry:** data/AI teams use Streamlit for **demos and internal tools**. Customer-facing products usually put the AI behind an **API (FastAPI)** with a separate frontend (React). You'll build that in S34.

**Interview line:** *"I used Streamlit for the demo UI. In production I'd put the logic behind a FastAPI service so any frontend can use it."*

---

## 6. Things to keep in mind (checklist)

1. **Run with `streamlit run`**, not `python`.
2. **Init state once:** `if "x" not in st.session_state: ...`
3. **Cache heavy things** (models, clients) with `@st.cache_resource`.
4. **Never cache per-user data** in `cache_resource`, or it leaks to other users.
5. **Never hardcode or commit API keys.** Use `st.secrets` and keep `secrets.toml` in `.gitignore`.
6. **Save the streamed answer** (`answer = st.write_stream(...)`) into history.
7. **Handle errors** (`try/except` around model calls) so users see a friendly message, not a stack trace.
8. **Pin your dependencies** in `requirements.txt`, because the cloud installs from it.
9. **Free apps sleep** when unused. Open your link before a demo or interview.

---

## 7. Lessons: run them in order

```bash
git clone https://github.com/nizam-farhaan/learn-streamlit.git
cd learn-streamlit
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install -r requirements.txt

streamlit run 01_hello.py
```

| # | File | You'll learn | API key? |
|---|---|---|---|
| 01 | `01_hello.py` | Display elements | No |
| 02 | `02_inputs.py` | Widgets return values | No |
| 03 | `03_rerun_model.py` | **The rerun model** (broken counter) | No |
| 04 | `04_session_state.py` | Memory across reruns (fixed counter) | No |
| 05 | `05_layout.py` | Sidebar, columns, tabs, expander | No |
| 06 | `06_caching.py` | Cache slow work (timed before/after) | No |
| 07 | `07_chat_basic.py` | Chat UI + vanishing-history bug | No |
| 08 | `08_streaming.py` | Streaming vs waiting | No |
| 09 | `09_ai_chatbot.py` | **Real Gemini chatbot** (deploy this one) | Yes |
| 10 | `10_file_upload.py` | Upload a PDF and summarize it with AI | Yes |

**API key setup (09, 10):** get a free key at [Google AI Studio](https://aistudio.google.com/apikey), then:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edit secrets.toml and paste your key
```

---

## 8. Deploy it

Step-by-step guide: **[docs/DEPLOY.md](docs/DEPLOY.md)**. Short version:
1. Push this repo to GitHub (secrets file is ignored).
2. Go to [share.streamlit.io](https://share.streamlit.io), create an app, and pick `09_ai_chatbot.py`.
3. Paste your key in **Advanced settings → Secrets**.
4. Deploy, then open the link on your phone. 🎉

---

## More
- 📄 [docs/CHEATSHEET.md](docs/CHEATSHEET.md): one-page revision
- 🎤 [docs/INTERVIEW_QA.md](docs/INTERVIEW_QA.md): interview questions with answers
- 📝 [docs/ASSIGNMENT.md](docs/ASSIGNMENT.md): take-home task
