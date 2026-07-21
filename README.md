# Naukri Profile Update

This repository contains a small automation script that updates a Naukri resume headline automatically using Playwright.

## What it does

- Opens the Naukri profile page in a headless browser
- Loads cookies from either:
  - the environment variable `NAUKRI_COOKIES`, or
  - the local file `cookie.json`
- Navigates to the Resume Headline section
- Toggles the trailing period in the headline and saves the change
- Prints a success or failure message for local runs and GitHub Actions

## Requirements

- Python 3.10+
- Playwright
- Playwright Stealth

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install playwright playwright-stealth
   ```

3. Install Playwright browsers:
   ```bash
   playwright install chromium
   ```

4. Add cookies:
   - Option A: set the environment variable `NAUKRI_COOKIES`
   - Option B: place a valid `cookie.json` file in the repo root

## Usage

Run the script locally:

```bash
python update_profile.py
```

## GitHub Actions workflow

This repository includes a workflow file at [.github/workflows/update.yml](.github/workflows/update.yml).

To use the same automation in another GitHub repository:

1. Copy the workflow file into your repo.
2. Add a secret named `NAUKRI_COOKIES` with a valid JSON array of cookies.
3. Enable the workflow from the Actions tab.
4. Optionally, run it manually with "Run workflow" or let it run on the schedule.

> The workflow uses the `NAUKRI_COOKIES` secret, so it does not rely on a local cookie file in GitHub.

## Notes

- The script is intended for personal automation and should be used carefully.
- Cookies may expire, so you may need to refresh them periodically.
- For GitHub Actions, the script runs headless and writes a summary message if supported.

## Files

- `update_profile.py` - main automation script
- `cookie.json` - local cookie backup file (if present)
- `tests/test_update_naukri.py` - basic regression tests
