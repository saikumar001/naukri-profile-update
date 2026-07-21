import os
import json
import time
import random
from pathlib import Path
from playwright.sync_api import sync_playwright

try:
    from playwright_stealth import Stealth
except ImportError:  # pragma: no cover - fallback for older installs
    Stealth = None

COOKIE_FILE = Path(__file__).with_name("cookie.json")


def load_cookies():
    """Helper function to load cookies from environment or local file."""
    cookies_json = os.environ.get("NAUKRI_COOKIES")
    if cookies_json:
        print("Loading cookies from environment variable.")
        return json.loads(cookies_json)

    if COOKIE_FILE.exists():
        with COOKIE_FILE.open("r", encoding="utf-8") as handle:
            print("Loading cookies from local file.")
            return json.load(handle)

    raise ValueError("No cookies found in environment variables or cookie.json.")


def update_naukri():
    # Wrap sync_playwright() with the Stealth context manager
    playwright_context = Stealth().use_sync(sync_playwright()) if Stealth else sync_playwright()
    
    with playwright_context as p:
        # Automatically run headless on GitHub Actions, but show UI when testing locally
        is_github_actions = os.environ.get("GITHUB_ACTIONS") == "true"
        browser = p.chromium.launch(headless=is_github_actions)
        
        # ⚠️ CRITICAL: Replace the string below with your exact User-Agent
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
        )
        
        # Load cookies using the helper function
        cookies = load_cookies()
        
        # Clean invalid sameSite attributes
        for cookie in cookies:
            if "sameSite" in cookie and cookie["sameSite"] not in ["Strict", "Lax", "None"]:
                del cookie["sameSite"]
                
        context.add_cookies(cookies)
        
        page = context.new_page()
        
        print("Navigating directly to Naukri profile...")
        page.goto("https://www.naukri.com/mnjuser/profile", timeout=60000)
        
        # Check if we were redirected back to the login page
        if "login" in page.url.lower():
            print("🚨 ERROR: Redirected to login page. Your session cookies have expired or are invalid.")
            print("Action needed: Export fresh cookies from your browser and update the GitHub Secret.")
            browser.close()
            return
            
        try:
            # Human pause: reading the page before acting
            time.sleep(random.uniform(1.0, 3.0))
            
            # Locate the Resume Headline section
            print("Locating Resume Headline widget...")
            widget = page.locator("div.widgetHead", has_text="Resume headline")
            
            # Human click delay on the edit button
            widget.locator("span.edit").click(delay=random.randint(50, 150))
            
            # Wait for the text area inside the popup to become visible
            textarea = page.locator("textarea#resumeHeadlineTxt")
            textarea.wait_for(state="visible")
            
            # Human pause: thinking time before typing
            time.sleep(random.uniform(0.5, 1.5))
            
            current_text = textarea.input_value()
            print(f"Current Headline: {current_text}")
            
            # The "Headline Hack": Toggle a period at the very end
            if current_text.endswith('.'):
                new_text = current_text[:-1]
                print("Action: Removing period.")
            else:
                new_text = current_text + '.'
                print("Action: Adding period.")
                
            # fill the textarea with the new headline
            textarea.fill(new_text)
            
            # Human pause: quick check before saving
            time.sleep(random.uniform(0.5, 1.0))
            
            # Click the Save button (using exact text match and a human click delay)
            page.locator("button:text-is('Save')").click(delay=random.randint(50, 150))
            
            # Give the browser a moment to process the network request
            time.sleep(3)
            print("✅ Profile successfully updated!")
            
            # Final pause so you can see the success state when testing locally
            if not is_github_actions:
                time.sleep(5)
            
        except Exception as e:
            print(f"❌ Failed to update profile. Error: {e}")
        
        finally:
            browser.close()

if __name__ == "__main__":
    update_naukri()