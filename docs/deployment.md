# Deployment Record — FocusFlow AI

Deployed: 2026-07-11  
Account: `806162193320`  
Region: `us-east-1`

## Live API

| Item | Value |
|---|---|
| API base | https://f4wluoskhh.execute-api.us-east-1.amazonaws.com |
| Generate plan | https://f4wluoskhh.execute-api.us-east-1.amazonaws.com/generate-plan |
| History | https://f4wluoskhh.execute-api.us-east-1.amazonaws.com/history |
| DynamoDB table | `FocusPlans` |
| Lambda | `focusflow-ai-challenge-generate-plan` |
| Lambda logs | `/aws/lambda/focusflow-ai-challenge-generate-plan` |

### Smoke test result

- `POST /generate-plan` — **200**, Bedrock Nova Lite returned priority/schedule/tip/motivation, saved to DynamoDB
- `GET /history` — **200**, returned the stored plan

## Amplify

| Item | Value |
|---|---|
| App name | `focusflow-ai-challenge` |
| App ID | `d1bmkxya6wd6tp` |
| Default domain | `d1bmkxya6wd6tp.amplifyapp.com` |
| Branch connected | **No** (repo not linked yet) |

Streamlit needs a long-running Python process. The Amplify **app shell** is provisioned with `API_BASE_URL` injected. To get a public Amplify URL:

1. Create a GitHub repository and push this project.
2. Amplify Console → app `focusflow-ai-challenge` → Hosting → Connect repository.
3. Set the monorepo/app root to `frontend`.
4. Use Dockerfile-based hosting if available in your Amplify experience; otherwise use local/Docker (below) or App Runner as compute.

See [amplify-deploy.md](amplify-deploy.md).

## Local frontend (works now)

```powershell
cd frontend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

`frontend/.streamlit/secrets.toml` already points at the live API.
