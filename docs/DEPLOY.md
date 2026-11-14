# Deploy to Streamlit Community Cloud (free)

Goal: a public URL like `https://your-app.streamlit.app` that works on any phone.

## Before you start
- [ ] App runs locally with `streamlit run 09_ai_chatbot.py`
- [ ] `requirements.txt` lists every library you import
- [ ] `.streamlit/secrets.toml` is in `.gitignore` (check with `git status`: it must NOT appear)
- [ ] A GitHub account and a free Gemini key

## Steps

**1. Push to GitHub**
```bash
git init
git add .
git commit -m "Streamlit AI chatbot"
git branch -M main
git remote add origin https://github.com/<your-username>/learn-streamlit.git
git push -u origin main
```
Then open the repo on GitHub and confirm `secrets.toml` is **not** there.

**2. Create the app**
1. Go to **share.streamlit.io** and sign in with GitHub.
2. Click **Create app** and choose to deploy from a GitHub repo.
3. Repository: `<your-username>/learn-streamlit`. Branch: `main`. Main file path: `09_ai_chatbot.py`.
4. Pick a custom subdomain if you want, e.g. `farhaan-ai-chatbot`.

**3. Add the secret**
Open **Advanced settings → Secrets** and paste the same TOML as your local file:
```toml
GEMINI_API_KEY = "your-real-key"
```
Your code reads it with `st.secrets["GEMINI_API_KEY"]`, exactly like it does locally.

**4. Deploy**
Click **Deploy**. The first build takes a few minutes while it installs `requirements.txt`.

**5. Test like a user**
- Open the link on your **phone**.
- Send 2 messages and check the history stays.
- Paste the link into your README and post it in the class chat.

## Updating your app
Push to `main` and the app redeploys automatically.

## Common errors

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError` | Library missing from `requirements.txt` | Add it, push again |
| `KeyError: GEMINI_API_KEY` / secrets not found | Secret not added on the cloud | App settings → Secrets |
| App shows "zzz" / takes long to open | Free apps sleep when unused | Click "wake up"; open it before demos |
| `429` / quota error | Free-tier rate limit hit | Wait a minute; keep demos short |
| Works locally, fails on cloud | Different library versions | Pin versions in `requirements.txt` |

## Security rules
1. **Never** commit a key. If you do, **revoke it immediately** in AI Studio and make a new one. Deleting the commit is not enough, because Git history keeps it.
2. A public app spends **your** quota. For a public demo, keep the free tier, or add the sidebar key input so visitors use their own key.
