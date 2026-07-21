# 🚀 Naukri Profile Auto-Updater

An automated bot built with Python and Playwright that logs into your Naukri account and makes a tiny update to your resume headline every day. This keeps your profile marked as "Recently Updated," keeping you at the top of recruiter search results!

## ✨ Features
* **100% Cloud-Based:** Runs entirely on GitHub Actions. No need to keep your PC on.
* **Stealthy:** Uses Playwright-Stealth and randomized human-like typing/clicking delays to avoid bot detection.
* **Secure:** Uses encrypted session cookies so your password is never exposed.
* **Verifiable:** Outputs a clean success/failure summary directly to the GitHub Actions dashboard.

## 🛠️ How to Set It Up for Yourself

### Step 1: Fork this Repository
Click the **Fork** button at the top right of this page to create your own private copy of this code. 

### Step 2: Get Your Naukri Cookies
We use cookies to safely bypass the login screen.
1. Download a cookie exporter extension for Chrome (like [Export cookie JSON file for Puppeteer/Playwright](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)).
2. Log into [Naukri.com](https://www.naukri.com) on your computer.
3. Click the extension to copy your session cookies to your clipboard.

### Step 3: Add Cookies to GitHub
1. In your forked repository, go to **Settings** > **Secrets and variables** > **Actions**.
2. Click **New repository secret**.
3. Name it exactly: `NAUKRI_COOKIES`
4. Paste your copied JSON cookies into the secret box and save.

### Step 4: Match Your User-Agent (Crucial for Anti-Bot)
To make the cloud server look exactly like your home computer, you need to match your User-Agent.
1. On the exact same browser you used to get your cookies, Google the phrase: **"What is my user agent"** (Google will show it at the very top of the search results).
2. Copy that entire string (it usually starts with `Mozilla/5.0...`).
3. In your GitHub repository, open `update_profile.py` and click the pencil icon to edit it.
4. Scroll down to around line 42 and replace my User-Agent string with yours:
   ```python
   context = browser.new_context(
       user_agent="PASTE_YOUR_USER_AGENT_HERE"
   )