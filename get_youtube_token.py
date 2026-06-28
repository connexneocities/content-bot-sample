"""
Run this script ONCE on your local computer to get your refresh token.
After that, paste the token into GitHub Secrets and never run this again.

HOW TO USE:
1. pip install google-auth-oauthlib
2. python get_youtube_token.py
3. A browser window opens -> login with Google -> allow access
4. Copy the refresh token printed in the terminal
5. Paste it as YOUTUBE_REFRESH_TOKEN in GitHub Secrets
"""

from google_auth_oauthlib.flow import InstalledAppFlow
import json

# Paste your Client ID and Client Secret here
CLIENT_ID     = "PASTE_YOUR_CLIENT_ID_HERE"
CLIENT_SECRET = "PASTE_YOUR_CLIENT_SECRET_HERE"

client_config = {
    "installed": {
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
        "auth_uri":      "https://accounts.google.com/o/oauth2/auth",
        "token_uri":     "https://oauth2.googleapis.com/token",
    }
}

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
creds = flow.run_local_server(port=0)

print("\n" + "="*50)
print("✅ SUCCESS! Your refresh token is:")
print("="*50)
print(creds.refresh_token)
print("="*50)
print("\nCopy the token above and add it to GitHub Secrets as YOUTUBE_REFRESH_TOKEN")
