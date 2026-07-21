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
1. Download a cookie exporter extension for Chrome (like [Export cookie JSON file for Puppeteer/Playwright](https://chrome.google.com/webstore/detail/export-cookie-json-file-f/nmckfnbeljlehmilbdamobohkahaemcl)).
2. Log into [Naukri.com](https://www.naukri.com) on your computer.
3. Click the extension to copy your session cookies to your clipboard.

### Step 3: Add Cookies to GitHub
1. In your forked repository, go to **Settings** > **Secrets and variables** > **Actions**.
2. Click **New repository secret**.
3. Name it exactly: `NAUKRI_COOKIES`
4. Paste your copied JSON cookies into the secret box and save.

### Step 4: Enable the Automation
1. Go to the **Actions** tab in your repository.
2. Click the green button that says "I understand my workflows, go ahead and enable them".
3. Click on **Update Naukri Profile** on the left.
4. Click **Run workflow** to test it!

*Note: By default, this runs automatically at 10 AM, 2 PM, and 5 PM IST, Monday through Friday. You can change this schedule in `.github/workflows/update.yml`.*