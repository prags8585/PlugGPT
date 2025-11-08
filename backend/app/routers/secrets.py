# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# import os, json

# router = APIRouter()

# class SecretsRequest(BaseModel):
#     project_name: str
#     values: dict

# @router.post("/secrets")
# def save_secrets(req: SecretsRequest):
#     # Demo-only: append to workspace/<project>/.env
#     try:
#         base = f"workspace/{req.project_name}/.env"
#         lines = []
#         for k, v in req.values.items():
#             lines.append(f"{k}={v}")
#         os.makedirs(os.path.dirname(base), exist_ok=True)
#         with open(base, "a", encoding="utf-8") as f:
#             f.write("\n".join(lines) + "\n")
#         return {"ok": True}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
from __future__ import annotations

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
    # Pick newest by mtime
    projects.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return projects[0]


class SecretsRequest(BaseModel):
    project_name: Optional[str] = None
    values: Dict[str, str] = {}  # optional; you can seed/override


class SecretsResponse(BaseModel):
    ok: bool
    result: Dict[str, str]


@router.post("/secrets", response_model=SecretsResponse)
def add_secrets(req: SecretsRequest) -> SecretsResponse:
    project_dir = (
        (WORKSPACE_ROOT / req.project_name)
        if req.project_name
        else latest_project_dir()
    )
    if not project_dir.exists():
        raise HTTPException(status_code=404, detail=f"Project not found: {project_dir.name}")

    env_path = project_dir / ".env"

    # If you have integration-aware templates, render them here.
    # For now we keep the common placeholders:
    lines = [
        "# Stripe",
        "STRIPE_SECRET_KEY=sk_test_replace",
        "STRIPE_WEBHOOK_SECRET=whsec_replace",
        "",
        "# Firebase",
        "FIREBASE_PROJECT_ID=your_project",
        "FIREBASE_CLIENT_EMAIL=svc@your_project.iam.gserviceaccount.com",
        "FIREBASE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\\nREPLACE\\n-----END PRIVATE KEY-----\\n",
        "",
        "# Add any other integration secrets below:",
    ]

    # Allow overrides from request
    for k, v in (req.values or {}).items():
        lines.append(f"{k}={v}")

    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return SecretsResponse(
        ok=True,
        result={"project_root": str(project_dir), "env": str(env_path)},
    )
