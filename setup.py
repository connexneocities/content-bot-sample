"""
ONE TIME SETUP SCRIPT
Run this once on your computer:
  pip install google-auth-oauthlib requests
  python setup.py

It will:
1. Open your browser to login with Google
2. Print your refresh token
3. You paste that token into GitHub Secrets as YOUTUBE_REFRESH_TOKEN
"""

import json
import webbrowser
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# ── Paste your values here ────────────────────────────────────────────────────
# Get these FREE in 2 minutes:
# 1. Go to: https://console.cloud.google.com
# 2. New project → Enable "YouTube Data API v3"
# 3. Credentials → Create OAuth Client ID → Desktop App
# 4. Copy Client ID and Client Secret below
CLIENT_ID     = "PASTE_CLIENT_ID_HERE"
CLIENT_SECRET = "PASTE_CLIENT_SECRET_HERE"
# ─────────────────────────────────────────────────────────────────────────────

REDIRECT_URI = "http://localhost:8080"
SCOPE = "https://www.googleapis.com/auth/youtube.upload"

auth_code = None

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        params = parse_qs(urlparse(self.path).query)
        auth_code = params.get("code", [None])[0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"<h1>Success! You can close this tab now.</h1>")
        threading.Thread(target=self.server.shutdown).start()

    def log_message(self, *args):
        pass  # silence logs

def main():
    auth_url = (
        f"https://accounts.google.com/o/oauth2/auth"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPE}"
        f"&response_type=code"
        f"&access_type=offline"
        f"&prompt=consent"
    )

    print("\n🌐 Opening browser for Google login...")
    print("   If browser doesn't open, visit this URL manually:")
    print(f"\n{auth_url}\n")
    webbrowser.open(auth_url)

    server = HTTPServer(("localhost", 8080), Handler)
    print("⏳ Waiting for you to login...")
    server.serve_forever()

    if not auth_code:
        print("❌ Login failed")
        return

    # Exchange code for tokens
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "code":          auth_code,
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri":  REDIRECT_URI,
        "grant_type":    "authorization_code",
    })

    tokens = r.json()
    refresh_token = tokens.get("refresh_token")

    if refresh_token:
        print("\n" + "="*60)
        print("✅ SUCCESS! Add these to GitHub Secrets:")
        print("="*60)
        print(f"\nYOUTUBE_CLIENT_ID     = {CLIENT_ID}")
        print(f"YOUTUBE_CLIENT_SECRET = {CLIENT_SECRET}")
        print(f"YOUTUBE_REFRESH_TOKEN = {refresh_token}")
        print("\n" + "="*60)

        # Save to .env file for reference
        with open(".env.example", "w") as f:
            f.write(f"YOUTUBE_CLIENT_ID={CLIENT_ID}\n")
            f.write(f"YOUTUBE_CLIENT_SECRET={CLIENT_SECRET}\n")
            f.write(f"YOUTUBE_REFRESH_TOKEN={refresh_token}\n")
        print("💾 Also saved to .env.example file")
    else:
        print(f"❌ Failed: {tokens}")

if __name__ == "__main__":
    main()
