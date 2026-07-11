# Amplify Deployment Notes

Streamlit is a Python web server, not a static site. Prefer **Dockerfile-based** hosting.

## Current Amplify resources (this account)

| Item | Value |
|---|---|
| App name | `focusflow-ai-challenge` |
| App ID | `d1bmkxya6wd6tp` |
| Default domain | `d1bmkxya6wd6tp.amplifyapp.com` |
| `API_BASE_URL` (injected by Terraform) | `https://f4wluoskhh.execute-api.us-east-1.amazonaws.com` |
| GitHub branch connected | Not yet |

Until a repository is connected and a Streamlit-capable build succeeds, use **local** or **Docker** hosting (below).

## Local run

```bash
cd frontend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# PowerShell:
$env:API_BASE_URL = "https://f4wluoskhh.execute-api.us-east-1.amazonaws.com"
# Or copy .streamlit/secrets.toml.example → secrets.toml

streamlit run app.py
```

## Docker run

```bash
cd frontend
docker build -t focusflow-frontend .
docker run --rm -p 8501:8501 \
  -e API_BASE_URL="https://f4wluoskhh.execute-api.us-east-1.amazonaws.com" \
  focusflow-frontend
```

## Connect GitHub → Amplify (public URL)

1. Create a GitHub repo and push this project (`git remote add origin …` · `git push -u origin main`).
2. AWS Console → **Amplify** → app **focusflow-ai-challenge**.
3. **Hosting** → **Connect repository** → authorize GitHub → select the repo/branch.
4. Set the app root / monorepo path to `frontend`.
5. Prefer a **Dockerfile** deploy path so Streamlit keeps a long-running process on port `8501`.
6. Confirm environment variable `API_BASE_URL` equals the API Gateway endpoint above.
7. Save & deploy. Copy the branch URL (e.g. `https://main.d1bmkxya6wd6tp.amplifyapp.com`).
8. Optionally set Terraform `cors_allow_origins` to that URL and re-apply.

If Amplify cannot host the Streamlit container in your account experience, run the Docker image on **App Runner** or **ECS Fargate** and keep the Amplify app for challenge write-up / future static assets.

## Runtime config

| Variable | Purpose |
|---|---|
| `API_BASE_URL` | API Gateway HTTP API base URL |
| `API_KEY` | Optional; unused unless API auth is added later |
