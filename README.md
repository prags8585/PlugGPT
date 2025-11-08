# PlugGPT — React UI + Terraform + Cloud Run Deployer

This package includes:
- **Backend (FastAPI)** with cloud deployer (gcloud shell-out)
- **React Frontend** (Vite + Tailwind, shadcn-like Button)
- **Terraform** templates for Cloud Run + Secret Manager
- **Generation Manifests & Templates** for Stripe + Firebase

## Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export GCP_PROJECT_ID=your-project-id
export GCP_REGION=us-central1   # optional
uvicorn app.main:app --reload --port 8000
```

## Frontend (React)
```bash
cd frontend-react
npm install
npm run dev
# visit http://localhost:5173
```

## Demo flow
1. Type a request like: "Add Firebase login and Stripe subscriptions and deploy to GCP"
2. Plan → Generate → Add Secrets (demo) in the UI
3. Run generated app locally:
```bash
cd workspace/demo_app
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # paste your real keys
uvicorn app.main:app --reload --port 8001
```
4. (Optional) Deploy to Cloud Run from the UI; backend will call `gcloud`:
```bash
# Make sure you have gcloud auth and project configured
gcloud auth login
gcloud config set project $GCP_PROJECT_ID
```

## Terraform
- For the generated app: see `workspace/demo_app/infra` (scaffolded)
- Root terraform (generic): `terraform/` folder provides a simple Cloud Run + Secret Manager setup.

> Note: The `/api/secrets` endpoint appends secrets to `.env` for demo convenience. Replace with Secret Manager in production.
