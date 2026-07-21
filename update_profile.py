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
            
            # Click the Save button
            page.locator("button:text-is('Save')").click(delay=random.randint(50, 150))
            
            # Pause to allow Naukri servers to process the save
            time.sleep(4)
            
            # --- VERIFICATION STAGE ---
            print("Verifying update...")
            
            # Refresh the page to clear any success popups and get fresh server data
            page.reload(wait_until="domcontentloaded")
            time.sleep(random.uniform(2.0, 4.0))
            
            # Re-locate the widget since the page reloaded
            widget = page.locator("div.widgetHead", has_text="Resume headline")
            
            # Click edit again
            widget.locator("span.edit").click(delay=random.randint(50, 150))
            
            # We need to re-declare the textarea locator after a page reload
            textarea = page.locator("textarea#resumeHeadlineTxt")
            textarea.wait_for(state="visible")
            
            saved_text = textarea.input_value()
            
            if saved_text == new_text:
                success_msg = f"### ✅ Profile successfully updated!\n**New Headline:**\n> {saved_text}"
                print(success_msg)
            else:
                success_msg = f"### ⚠️ Warning: Profile might not have updated correctly.\n**Expected:** {new_text}\n**Found:** {saved_text}"
                print(success_msg)

            # Write the result to the GitHub Actions UI dashboard
            summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
            if summary_file:
                with open(summary_file, "a", encoding="utf-8") as f:
                    f.write(success_msg)
            
            if not is_github_actions:
                time.sleep(5)
            
        except Exception as e:
            error_msg = f"### ❌ Failed to update profile.\n**Error:** `{e}`"
            print(error_msg)
            
            summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
            if summary_file:
                with open(summary_file, "a", encoding="utf-8") as f:
                    f.write(error_msg)
        
        finally:
            browser.close()

if __name__ == "__main__":
    update_naukri()