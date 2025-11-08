# Local and Cloud Run deployer. Cloud Run requires gcloud CLI configured.
import os, subprocess, shlex

def deploy_local(project_name: str) -> str:
    return "http://localhost:8001"

def _run(cmd: str):
    print(f"[deployer] $ {cmd}")
    proc = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    return proc.stdout.strip()

def deploy_cloud_run(project_name: str) -> str:
    project_id = os.getenv("GCP_PROJECT_ID")
    region = os.getenv("GCP_REGION", "us-central1")
    if not project_id:
        raise RuntimeError("Set GCP_PROJECT_ID env var for backend before calling cloud_run deploy")
    image = f"gcr.io/{project_id}/{project_name}"
    # Build & push image
    _run(f"gcloud builds submit --tag {image}")
    # Deploy
    _run(f"gcloud run deploy {project_name} --image {image} --region {region} --allow-unauthenticated")
    # Get URL
    url = _run(f"gcloud run services describe {project_name} --region {region} --format=value(status.url)")
    return url
