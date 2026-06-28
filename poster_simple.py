"""
SIMPLEST YOUTUBE UPLOAD - Using your Google account directly
No Google Cloud, No API Console, No OAuth Playground

Uses selenium to upload like a real human would.
Just needs your Google email and password as GitHub Secrets.
"""

import os
import time

GOOGLE_EMAIL    = os.environ.get("GOOGLE_EMAIL", "")
GOOGLE_PASSWORD = os.environ.get("GOOGLE_PASSWORD", "")


def upload_to_youtube_selenium(video_path, title, description):
    """Upload to YouTube by automating the browser like a human"""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.keys import Keys
        import pyautogui

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        print("🌐 Opening browser...")
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 30)

        # Login to Google
        print("🔐 Logging into Google...")
        driver.get("https://accounts.google.com/signin")
        time.sleep(2)

        # Enter email
        email_field = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
        email_field.send_keys(GOOGLE_EMAIL)
        email_field.send_keys(Keys.RETURN)
        time.sleep(2)

        # Enter password
        password_field = wait.until(EC.presence_of_element_located((By.NAME, "Passwords")))
        password_field.send_keys(GOOGLE_PASSWORD)
        password_field.send_keys(Keys.RETURN)
        time.sleep(3)

        # Go to YouTube Studio
        print("📺 Going to YouTube Studio...")
        driver.get("https://studio.youtube.com")
        time.sleep(3)

        # Click Upload button
        upload_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//ytcp-button[@id='upload-icon']")))
        upload_btn.click()
        time.sleep(2)

        # Select file
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        file_input.send_keys(os.path.abspath(video_path))
        print(f"📁 Uploading file: {video_path}")
        time.sleep(5)

        # Fill title
        title_field = wait.until(EC.presence_of_element_located((By.XPATH, "//ytcp-social-suggestions-textbox[@id='title-textarea']//div[@contenteditable]")))
        title_field.clear()
        title_field.send_keys(title[:100])

        # Fill description
        desc_field = driver.find_element(By.XPATH, "//ytcp-social-suggestions-textbox[@id='description-textarea']//div[@contenteditable]")
        desc_field.send_keys(description + "\n\n#Shorts #News #Trending")

        # Click Next 3 times
        for i in range(3):
            next_btn = wait.until(EC.element_to_be_clickable((By.ID, "next-button")))
            next_btn.click()
            time.sleep(2)

        # Set public
        public_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//tp-yt-paper-radio-button[@name='PUBLIC']")))
        public_btn.click()
        time.sleep(1)

        # Publish
        publish_btn = wait.until(EC.element_to_be_clickable((By.ID, "done-button")))
        publish_btn.click()
        time.sleep(5)

        print("✅ YouTube video uploaded successfully!")
        driver.quit()
        return True

    except Exception as e:
        print(f"❌ Selenium upload error: {e}")
        try:
            driver.quit()
        except:
            pass
        return False


if __name__ == "__main__":
    result = upload_to_youtube_selenium(
        "output/test.mp4",
        "Test Video",
        "Test description"
    )
    print("Result:", result)
