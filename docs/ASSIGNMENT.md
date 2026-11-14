# Assignment: Ship Your Own AI App

**Goal:** a live link to an AI app *you* customised, in your GitHub README.

## Tasks
1. **Pick a persona.** Change `SYSTEM_PROMPT` in `09_ai_chatbot.py` to something useful, e.g. an interview coach, a Python tutor or a recipe helper. Rename the title to match.
2. **Add a sidebar control** that changes behaviour, e.g. a "Short / Detailed" radio or a temperature slider. Pass it into the model call.
   *Hint:* `config={"system_instruction": ..., "temperature": temp}`
3. **Add a "Download chat" button** that saves the conversation as a `.txt` file.
   *Hint:* `st.download_button("Download", data=text, file_name="chat.txt")`
4. **Deploy** to Streamlit Community Cloud using [DEPLOY.md](DEPLOY.md).
5. **README:** add the live link and one screenshot.

## Submit
Post your live link in the class chat.

## Stretch (optional)
- Plug in **your own backend** from an earlier session (e.g. your RAG function) instead of the plain Gemini call.
- Add a 👍/👎 button under each answer and save the feedback to `session_state`.

## Checklist before you submit
- [ ] Opens on a phone
- [ ] History survives 3+ messages
- [ ] No API key in your GitHub repo
- [ ] Friendly error if the model call fails
