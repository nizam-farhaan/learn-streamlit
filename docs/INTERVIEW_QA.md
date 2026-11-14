# Interview Q&A: Streamlit and Deploying AI Apps

**1. How does Streamlit work under the hood?**
On every user interaction, Streamlit reruns the whole script top to bottom. Widgets return their new values on that run, and the browser updates only what changed. The browser and server stay connected through a WebSocket, and each tab gets its own session.

**2. Why does Streamlit lose state between interactions, and how does `session_state` fix it?**
Because the script reruns, normal variables are re-created on every run (`messages = []` resets). `st.session_state` is a per-session dictionary kept on the server that survives reruns. You initialise it once with `if "key" not in st.session_state`. It does not survive a page refresh, so long-term history needs a database.

**3. `st.cache_resource` vs `st.cache_data`?**
`cache_resource` is for objects you load or connect once and share: ML models, DB connections, LLM clients. Every caller gets the same object. `cache_data` is for data and results (DataFrames, API responses). It's keyed by the function arguments and returns a copy. Both are shared across all users, so never cache per-user data.

**4. What UX challenges come with streaming LLM responses?**
Streaming cuts time to first token, so the app feels faster, but total time stays the same. Challenges:
- You can't run output guardrails before the user sees the text.
- Errors can cut an answer off mid-sentence.
- Structured output (JSON) is invalid until complete.
- You must save the final text to history.

**5. How do you keep API keys safe in a public demo?**
Never hardcode or commit them. Locally, use `.streamlit/secrets.toml` (git-ignored). In the cloud, paste them into the platform's secrets settings and read them with `st.secrets`. If a key leaks, revoke it at once, because Git history keeps it even after deletion. For public demos, watch quota, or let visitors enter their own key.

**6. Would you use Streamlit in production?**
For internal tools and demos, yes. For a customer-facing product, I'd put the AI logic behind a FastAPI service so web, mobile and other apps can all call it. Then I'd use a dedicated frontend, because Streamlit's rerun model and limited UI control don't fit high-traffic public apps.

**7. Your Streamlit chatbot takes 6 seconds per reply. How do you debug it?**
First, check whether the model or client is loaded at the top level without caching. That's the most common cause, since it reloads on every rerun. Then time each step (retrieval vs LLM call). Use streaming to improve perceived latency, and consider a smaller or faster model.

**8. How does the chatbot "remember" earlier messages?**
There are two separate memories. `session_state` stores history for the **UI** to redraw. The **model** only remembers if you send that history in the request. If you show history but send only the last message, follow-ups like "explain that simpler" break.
