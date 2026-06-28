import os
from poster_simple import upload_to_youtube_selenium

GOOGLE_EMAIL    = os.environ.get("GOOGLE_EMAIL", "")
GOOGLE_PASSWORD = os.environ.get("GOOGLE_PASSWORD", "")


def post_to_all_platforms(video_path, script_data):
    results = {}

    title       = script_data.get("title", "Breaking News")
    caption     = script_data.get("caption", "")

    print("\n🚀 Posting to YouTube...")
    results["youtube"] = upload_to_youtube_selenium(video_path, title, caption)

    print("\n📊 Posting Summary:")
    for platform, success in results.items():
        icon = "✅" if success else "❌"
        print(f"   {icon} {platform.capitalize()}")

    return results
