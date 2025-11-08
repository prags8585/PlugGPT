# from fastapi import APIRouter, HTTPException
# from ..services.deployer import deploy_local, deploy_cloud_run

# router = APIRouter()

# @router.post("/deploy")
# def deploy_endpoint(project_name: str = "demo_app", target: str = "local"):
#     try:
#         if target == "cloud_run":
#             url = deploy_cloud_run(project_name)
#             return {"ok": True, "url": url}
#         url = deploy_local(project_name)
#         return {"ok": True, "url": url}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

WORKSPACE_ROOT = Path(__file__).resolve().parents[2] / "workspace"
WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)

router = APIRouter()


def latest_project_dir() -> Path:
    projects = [p for p in WORKSPACE_ROOT.iterdir() if p.is_dir()]
    if not projects:
        raise HTTPException(status_code=404, detail="No projects found in workspace")
    projects.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return projects[0]


class DeployRequest(BaseModel):
    project_name: Optional[str] = None
    mode: str = "local"  # or "cloudrun"
    extra: Dict[str, str] = {}


class DeployResponse(BaseModel):
    ok: bool
    result: Dict[str, str]


@router.post("/deploy", response_model=DeployResponse)
def deploy(req: DeployRequest) -> DeployResponse:
    project_dir = (
        (WORKSPACE_ROOT / req.project_name)
        if req.project_name
        else latest_project_dir()
    )
    if not project_dir.exists():
        raise HTTPException(status_code=404, detail=f"Project not found: {project_dir.name}")

    # ⚠️ Replace this with your real deploy logic.
    # Below is a harmless stub so the endpoint returns something useful.
    # Example: build a container, run docker compose, or trigger Cloud Run.
    result = {
        "project_root": str(project_dir),
        "mode": req.mode,
        "message": "Stub deploy OK. Replace with actual Docker/Cloud Run flow.",
    }

    # Example (commented):
    # if req.mode == "local":
    #     subprocess.check_call(["docker", "build", "-t", "plugapp", "."], cwd=project_dir)
    # elif req.mode == "cloudrun":
    #     subprocess.check_call(["bash", "deploy_cloud_run.sh"], cwd=project_dir)

    return DeployResponse(ok=True, result=result)
