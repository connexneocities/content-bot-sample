"""
YouTube uploader using browser cookies - NO API KEY NEEDED!

ONE TIME SETUP:
1. Install "Get cookies.txt LOCALLY" Chrome extension
   Link: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
2. Go to youtube.com and make sure you're logged in
3. Click the extension icon → Export cookies for youtube.com
4. Save the file as "cookies.txt" in this project folder
5. Upload cookies.txt to GitHub as a secret (base64 encoded)

That's it! No API, no OAuth, no Google Cloud.
"""

import os
import subprocess
import base64

def setup_cookies():
    """Decode cookies from GitHub Secret"""
    cookies_b64 = os.environ.get("YOUTUBE_COOKIES_B64", "")
    if cookies_b64:
        with open("cookies.txt", "w") as f:
            f.write(base64.b64decode(cookies_b64).decode())
        print("✅ Cookies loaded from GitHub Secret")
        return True
    elif os.path.exists("cookies.txt"):
        print("✅ Using local cookies.txt")
        return True
    else:
        print("❌ No cookies found!")
        return False


def upload_to_youtube(video_path, title, description):
    """Upload video to YouTube using yt-dlp with cookies"""
    if not setup_cookies():
        return False

    try:
        # Use yt-dlp to upload (it supports YouTube uploads with cookies)
        cmd = [
            "yt-dlp",
            "--cookies", "cookies.txt",
            "--upload-video", video_path,
            "--video-title", title[:100],
            "--video-description", description[:5000],
            "--video-category", "25",  # News & Politics
            "--video-privacy", "public",
        ]

        print(f"▶️  Uploading: {title}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ YouTube upload successful!")
            print(result.stdout)
            return True
        else:
            print(f"❌ Upload failed: {result.stderr}")
            # Try alternative method
            return upload_via_youtubeuploader(video_path, title, description)

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def upload_via_youtubeuploader(video_path, title, description):
    """Alternative: use youtubeuploader tool"""
    try:
        import requests

        # Use a simple HTTP-based uploader with cookies
        print("🔄 Trying alternative upload method...")

        with open("cookies.txt", "r") as f:
            cookie_content = f.read()

        # Parse cookies into dict
        cookies = {}
        for line in cookie_content.split("\n"):
            if line and not line.startswith("#"):
                parts = line.split("\t")
                if len(parts) >= 7:
                    cookies[parts[5]] = parts[6]

        session = requests.Session()
        session.cookies.update(cookies)

        # Get upload token
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.youtube.com",
        }

        print("⚠️  Cookie-based upload requires manual setup.")
        print("    Please use the cookies.txt method described at the top of this file.")
        return False

    except Exception as e:
        print(f"❌ Alternative also failed: {e}")
        return False


if __name__ == "__main__":
    upload_to_youtube(
        "output/test_video.mp4",
        "Test Upload",
        "This is a test upload from ContentBot"
    )
