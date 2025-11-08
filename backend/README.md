# PlugGPT Backend — React + Cloud enhancements

New in this version:
- Real **Cloud Run deployer** that shells to `gcloud` (requires `GCP_PROJECT_ID` env and gcloud auth)
- Terraform templates include **Cloud Run + Secret Manager** resources
- Frontend upgraded to **React + Vite + Tailwind + shadcn-style** UI (in `/frontend-react`)

## Run
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# For Cloud Run deploys:
export GCP_PROJECT_ID=your-project-id
export GCP_REGION=us-central1
uvicorn app.main:app --reload --port 8000
```
