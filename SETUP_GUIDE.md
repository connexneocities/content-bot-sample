# 🚀 Setup Guide — 10 Minutes Total

## What you need to do ONCE on your computer, then never again.

---

## STEP 1 — Get YouTube Client ID & Secret (5 min)

1. Go to: https://console.cloud.google.com
2. Click "Select a project" (top) → "New Project" → name it `ContentBot` → Create
3. Left menu → "APIs & Services" → "Library"
4. Search "YouTube Data API v3" → click it → click "Enable"
5. Left menu → "Credentials" → "+ Create Credentials" → "OAuth client ID"
6. If asked about consent screen:
   - Click "Configure consent screen" → "External" → Create
   - App name: ContentBot | Your email | Save → Continue → Continue → Continue → Back to dashboard
7. Back to Credentials → "+ Create Credentials" → "OAuth client ID"
8. Application type: **Desktop app**
9. Name: ContentBot → Create
10. A popup shows → copy **Client ID** and **Client Secret**

---

## STEP 2 — Run setup.py on your computer (2 min)

1. Open `setup.py` in any text editor
2. Paste your Client ID and Client Secret at the top
3. Open Command Prompt / Terminal in this folder
4. Run:
```
pip install requests
python setup.py
```
5. Browser opens → login with your Google account → click Allow
6. Terminal prints 3 values → copy them all

---

## STEP 3 — Add secrets to GitHub (3 min)

Go to your GitHub repo → Settings → Secrets → Actions → New secret

Add these:

| Secret Name | Value |
|---|---|
| `GEMINI_API_KEY` | from Google AI Studio |
| `YOUTUBE_CLIENT_ID` | printed by setup.py |
| `YOUTUBE_CLIENT_SECRET` | printed by setup.py |
| `YOUTUBE_REFRESH_TOKEN` | printed by setup.py |

---

## STEP 4 — Test it!

1. Go to GitHub repo → Actions tab
2. Click "Content Bot - Auto Post"
3. Click "Run workflow" → "Run workflow"
4. Watch it run — check your YouTube channel after!

---

## That's it! 🎉

The bot will now post automatically 4x per day to YouTube.
No more setup needed ever.

