# Streamlit Cloud Setup

Use this setup if you want `asportfoliotracker.streamlit.app` to keep portfolio data online without running the app from your laptop.

## 1. Create a Google Sheet

- Create one Google Sheet dedicated to the app.
- Copy the sheet ID from the URL.

## 2. Create a Google Service Account

- In Google Cloud, create or reuse a project.
- Enable the Google Sheets API.
- Create a service account.
- Generate a JSON key for that service account.

## 3. Share the Google Sheet

- Open the sheet.
- Share it with the service account email from the JSON key.
- Give it Editor access.

## 4. Configure Streamlit Secrets

In Streamlit app settings, open `Secrets` and paste values matching `.streamlit/secrets.toml.example`.

Required top-level keys:

- `google_sheet_id`
- `[google_service_account]`

## 5. Deploy

- Push this repo to GitHub.
- Make sure Streamlit Cloud deploys from `app.py`.
- Open the app URL and check the sidebar.

If everything is configured, the sidebar should show Google Sheets as the active storage.
