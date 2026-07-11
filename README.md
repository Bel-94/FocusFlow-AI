# FocusFlow AI

**An AI-powered productivity planner that transforms a user's daily brain dump into a prioritized action plan using Amazon Bedrock.**

Built for the AWS Builder Center Weekend Productivity Challenge — simple enough for a one-day build, structured like a production serverless service.

---

## Project Overview

FocusFlow AI accepts a free-form list of tasks, sends them to **Amazon Bedrock (Nova Lite)** through a serverless API, and returns:

- Prioritized task order
- Suggested schedule / focus blocks
- One practical focus tip
- One short motivational message

Plans are stored in **DynamoDB** so users can revisit history from the Streamlit UI.

| Layer | Technology |
|---|---|
| Frontend | Python · Streamlit · Amplify Hosting (app shell) |
| API | API Gateway HTTP API |
| Compute | AWS Lambda (Python 3.12) |
| AI | Amazon Bedrock — Nova Lite |
| Data | DynamoDB (`FocusPlans`) |
| Observability | CloudWatch Logs |
| IaC | Terraform |

---

## Architecture Diagram

```text
┌─────────────────────┐
│  Streamlit Frontend │  (local / Amplify / Docker)
└──────────┬──────────┘
           │  HTTPS
           ▼
┌─────────────────────┐
│ API Gateway HTTP API│  POST /generate-plan · GET /history
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   AWS Lambda 3.12   │──────────────────────────────┐
└──────────┬──────────┘                              │
           │                                         ▼
           │                              ┌─────────────────────┐
           │                              │ Amazon Bedrock      │
           │                              │ Nova Lite           │
           │                              └─────────────────────┘
           ▼
┌─────────────────────┐       ┌─────────────────────┐
│ DynamoDB FocusPlans │       │  CloudWatch Logs    │
└─────────────────────┘       └─────────────────────┘
```

Detailed design (Mermaid, data model, failure modes): [docs/architecture.md](docs/architecture.md)

---

## AWS Services

| Service | Role |
|---|---|
| **Amazon Bedrock** | Nova Lite generates structured productivity plans (JSON) |
| **API Gateway HTTP API** | Public HTTPS endpoints with CORS and throttling |
| **AWS Lambda** | Validates input, invokes Bedrock, writes DynamoDB, returns JSON |
| **Amazon DynamoDB** | Stores plans (`planId` PK, on-demand billing) |
| **Amazon CloudWatch** | Lambda + API access logs (14-day retention) |
| **AWS Amplify** | Frontend app shell + `API_BASE_URL` env (connect GitHub for hosting) |
| **IAM** | Least-privilege Lambda role (Bedrock + DynamoDB + Logs only) |

---

## Features

1. Paste today’s brain dump into a large text area
2. Click **Generate Plan**
3. View Priority, Schedule, Focus Tip, and Motivation
4. Browse previous plans on the **History** page
5. Serverless backend with structured logging and graceful error handling

---

## Live Deployment (`us-east-1`)

| Resource | Value |
|---|---|
| API base | https://f4wluoskhh.execute-api.us-east-1.amazonaws.com |
| Generate plan | `POST /generate-plan` |
| History | `GET /history` |
| DynamoDB | `FocusPlans` |
| Lambda | `focusflow-ai-challenge-generate-plan` |
| Amplify app | `focusflow-ai-challenge` (`d1bmkxya6wd6tp.amplifyapp.com`) |

Smoke-tested: Bedrock plan generation + DynamoDB persistence + history read.

Full record: [docs/deployment.md](docs/deployment.md)

---

## Folder Structure

```text
FocusFlow-AI/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── architecture.md
│   ├── amplify-deploy.md
│   └── deployment.md
├── screenshots/
├── frontend/
│   ├── app.py                 # Home — generate plan
│   ├── styles.py              # Brand / layout CSS
│   ├── api_client.py          # API Gateway client
│   ├── pages/1_History.py     # History page
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .streamlit/
├── backend/
│   ├── lambda_function.py     # Router + handlers
│   ├── bedrock.py             # Bedrock Converse client
│   ├── prompt.py              # Productivity-coach prompts
│   ├── dynamodb.py            # Persistence
│   ├── models.py              # Types + validation
│   ├── utils.py               # Logging + HTTP helpers
│   └── requirements.txt
└── terraform/
    ├── provider.tf
    ├── variables.tf
    ├── outputs.tf
    ├── main.tf
    ├── iam.tf
    ├── lambda.tf
    ├── apigateway.tf
    ├── dynamodb.tf
    ├── cloudwatch.tf
    ├── amplify.tf
    └── terraform.tfvars.example
```

---

## Deployment

### Prerequisites

1. AWS account with CLI credentials configured
2. Terraform `>= 1.5`
3. **Bedrock model access** enabled for Nova Lite in the target region
4. Python 3.12+ (local frontend)

### Backend (Terraform)

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edit region / names if needed
terraform init
terraform plan
terraform apply
```

Copy outputs:

```bash
terraform output api_endpoint
terraform output amplify_app_id
```

### Frontend — local (ready now)

```bash
cd frontend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# Option A — env var
# PowerShell: $env:API_BASE_URL = "https://f4wluoskhh.execute-api.us-east-1.amazonaws.com"
# Option B — secrets.toml (see .streamlit/secrets.toml.example)

streamlit run app.py
```

Open http://localhost:8501

### Frontend — Amplify public URL

Amplify app shell is already created. Connect a GitHub repository to publish:

1. Push this project to GitHub
2. Amplify Console → `focusflow-ai-challenge` → connect repo
3. Set app root to `frontend`
4. Prefer Dockerfile-based hosting for Streamlit
5. Confirm `API_BASE_URL` matches the API Gateway endpoint

Step-by-step: [docs/amplify-deploy.md](docs/amplify-deploy.md)

### Frontend — Docker

```bash
cd frontend
docker build -t focusflow-frontend .
docker run --rm -p 8501:8501 \
  -e API_BASE_URL="https://f4wluoskhh.execute-api.us-east-1.amazonaws.com" \
  focusflow-frontend
```

---

## Terraform Commands

| Command | Purpose |
|---|---|
| `terraform init` | Download providers |
| `terraform fmt` | Format `.tf` files |
| `terraform validate` | Validate configuration |
| `terraform plan` | Preview changes |
| `terraform apply` | Create / update stack |
| `terraform output` | Print API URL, Amplify ID, etc. |
| `terraform destroy` | Tear down (challenge cleanup) |

All values are parameterized via `variables.tf` / `terraform.tfvars`. Do not commit `terraform.tfvars`.

---

## Running Locally

### API (already in AWS)

Use the live endpoint above, or re-apply Terraform in your account.

### Streamlit UI

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### Example API calls

```bash
curl -X POST "https://f4wluoskhh.execute-api.us-east-1.amazonaws.com/generate-plan" \
  -H "Content-Type: application/json" \
  -d "{\"tasks\":\"- Finish AWS article\\n- Study Terraform\\n- Grocery shopping\"}"

curl "https://f4wluoskhh.execute-api.us-east-1.amazonaws.com/history"
```

---

## Environment Variables

### Lambda (set by Terraform)

| Variable | Description |
|---|---|
| `TABLE_NAME` | DynamoDB table (`FocusPlans`) |
| `BEDROCK_MODEL_ID` | Default `amazon.nova-lite-v1:0` |
| `HISTORY_LIMIT` | Max history items (default `20`) |
| `MAX_TASKS_CHARS` | Input size cap (default `4000`) |
| `LOG_LEVEL` | `INFO` / `DEBUG` |

### Streamlit frontend

| Variable | Description |
|---|---|
| `API_BASE_URL` | API Gateway base URL (no trailing slash) |
| `API_KEY` | Optional; unused unless you add auth later |

Or use `frontend/.streamlit/secrets.toml` (gitignored).

---

## API Contract

### `POST /generate-plan`

```json
{ "tasks": "- Finish AWS article\n- Study Terraform" }
```

```json
{
  "priority": ["..."],
  "schedule": ["..."],
  "focus_tip": "...",
  "motivation": "...",
  "planId": "...",
  "createdAt": "2026-07-11T11:31:42Z"
}
```

### `GET /history`

```json
{ "plans": [ { "planId": "...", "tasks": "...", "priority": [], "schedule": [], "focus_tip": "...", "motivation": "...", "createdAt": "..." } ] }
```

---

## Security Notes

- IAM least privilege — no `AdministratorAccess`
- No secrets in source code
- DynamoDB SSE enabled; table not publicly exposed
- CORS configurable; tighten `cors_allow_origins` to the Amplify URL after go-live
- Input length limited to control Bedrock cost

---

## Future Improvements

- Cognito auth + per-user plan partitioning
- DynamoDB GSI on `createdAt` (replace Scan)
- Bedrock Guardrails for safer outputs
- Custom domain + HTTPS on Amplify / App Runner
- CI/CD (GitHub Actions → Terraform + Amplify)
- X-Ray tracing and structured metrics dashboards
- WAF rate limits on the HTTP API

---

## Challenge Demo Script

1. Open Streamlit → paste a brain dump → **Generate Plan**
2. Show Priority / Schedule / Tip / Motivation
3. Open **History** → confirm the plan was saved
4. Optionally show CloudWatch logs and the DynamoDB item in the AWS console

---

## License

MIT — see [LICENSE](LICENSE).
