# Verification Guide — FocusFlow AI

## URLs

| What | URL |
|---|---|
| GitHub repo | https://github.com/Bel-94/FocusFlow-AI |
| Live API base | https://f4wluoskhh.execute-api.us-east-1.amazonaws.com |
| Generate plan | https://f4wluoskhh.execute-api.us-east-1.amazonaws.com/generate-plan |
| History | https://f4wluoskhh.execute-api.us-east-1.amazonaws.com/history |
| Amplify app (shell) | App ID `d1bmkxya6wd6tp` · domain `d1bmkxya6wd6tp.amplifyapp.com` |
| Local Streamlit UI | http://localhost:8501 |

> **Amplify GitHub connect** needs a one-time GitHub authorization (console OAuth) or a Personal Access Token. The Amplify **app shell** is already in AWS with `API_BASE_URL` set. Until a branch is connected/built, use the local Streamlit UI + live API for demos.

## Screenshots (proof)

Saved under `screenshots/`:

| File | Shows |
|---|---|
| `01-home.png` | Streamlit home + brain dump |
| `02-generated-plan.png` | Bedrock plan (priority/schedule/tip) |
| `03-history.png` | History page from DynamoDB |
| `04-github-repo.png` | Code on GitHub |
| `api-history-raw.json` | Live `GET /history` response |

## Tests you can run

### 1) API — generate plan (PowerShell)

```powershell
$api = "https://f4wluoskhh.execute-api.us-east-1.amazonaws.com"
$body = @{ tasks = "- Finish AWS article`n- Study Terraform`n- Grocery shopping" } | ConvertTo-Json
Invoke-RestMethod -Uri "$api/generate-plan" -Method POST -Body $body -ContentType "application/json"
```

Expect: JSON with `priority`, `schedule`, `focus_tip`, `motivation`, `planId`, `createdAt`.

### 2) API — history

```powershell
Invoke-RestMethod -Uri "$api/history" -Method GET
```

Expect: `{ plans: [ ... ] }` including the plan you just created.

### 3) API — validation

```powershell
Invoke-WebRequest -Uri "$api/generate-plan" -Method POST -Body '{"tasks":""}' -ContentType "application/json"
```

Expect: HTTP 400 with an error about empty tasks.

### 4) UI — local Streamlit

```powershell
cd frontend
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

1. Open http://localhost:8501  
2. Click **Generate Plan**  
3. Confirm Priority / Schedule / Focus tip / Motivation  
4. Open **History** and refresh  

### 5) AWS console checks

- Lambda: `focusflow-ai-challenge-generate-plan`
- DynamoDB table: `FocusPlans`
- API Gateway HTTP API: `focusflow-ai-challenge-http-api`
- Amplify app: `focusflow-ai-challenge`
- CloudWatch log group: `/aws/lambda/focusflow-ai-challenge-generate-plan`

## Finish Amplify public URL (needs your GitHub auth)

1. Open: https://us-east-1.console.aws.amazon.com/amplify/apps/d1bmkxya6wd6tp/overview  
2. **Hosting** → **Connect repository** → authorize GitHub → select `Bel-94/FocusFlow-AI` · branch `main`  
3. App root: `frontend`  
4. Confirm env `API_BASE_URL=https://f4wluoskhh.execute-api.us-east-1.amazonaws.com`  
5. Deploy  

**Or** send a GitHub PAT (repo scope) and I can finish the Amplify link via CLI:

```powershell
$env:GITHUB_TOKEN = "ghp_..."   # do not commit this
```

Then tell me to continue Amplify connect.
