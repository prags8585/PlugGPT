# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import Dict, Any
# from ..services.codegen import generate_project

# router = APIRouter()

# class GenerateRequest(BaseModel):
#     plan: Dict[str, Any]
#     project_name: str = "demo_app"

# @router.post("/generate")
# def generate_endpoint(req: GenerateRequest):
#     try:
#         result = generate_project(req.plan, req.project_name)
#         return {"ok": True, "result": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
# 20 - 157
# from __future__ import annotations

# import re
# from datetime import datetime
# from pathlib import Path
# from typing import Any, Dict, Optional

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel

# # ────────────────────────────────────────────────────────────────────────────────
# # Workspace root (…/backend/workspace)
# # Adjust if your layout differs
# # ────────────────────────────────────────────────────────────────────────────────
# WORKSPACE_ROOT = Path(__file__).resolve().parents[2] / "workspace"
# WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)

# # Known tokens we can extract from plan/prompt to make a nice project name
# KNOWN_KEYS = {
#     "firebase": "firebase",
#     "stripe": "stripe",
#     "supabase": "supabase",
#     "postgres": "postgres",
#     "telnyx": "telnyx",
#     "twilio": "twilio",
#     "comet": "comet",
#     "comet_ml": "comet",
#     "openai": "openai",
#     "gemini": "gemini",
#     "gcp": "gcp",
#     "cloud run": "cloudrun",
# }


# def slugify(s: str) -> str:
#     s = s.lower()
#     s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
#     return re.sub(r"-{2,}", "-", s)


# def tokens_from_prompt(prompt: Optional[str]) -> list[str]:
#     if not prompt:
#         return []
#     p = prompt.lower()
#     found: list[str] = []
#     for k, token in KNOWN_KEYS.items():
#         if k in p:
#             found.append(token)
#     return found


# def derive_project_name(plan: Dict[str, Any], prompt: Optional[str]) -> str:
#     names: list[str] = []

#     # Prefer integration names from plan
#     for itg in (plan.get("integrations") or []):
#         n = (itg.get("name") or "").strip()
#         if n:
#             names.append(slugify(n))

#     # If plan didn’t list integrations clearly, try the prompt
#     if not names:
#         names = tokens_from_prompt(prompt)

#     # Build readable base
#     base = "-".join(sorted(set(names))) if names else "project"
#     if base in ("", "-", "project"):
#         base = f"project-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

#     base = slugify(base)[:48]
#     if not base.endswith("-app"):
#         base = f"{base}-app"

#     # Ensure uniqueness (…/workspace/<name>, <name>-2, <name>-3, …)
#     candidate = base
#     i = 2
#     while (WORKSPACE_ROOT / candidate).exists():
#         candidate = f"{base}-{i}"
#         i += 1
#     return candidate


# # ────────────────────────────────────────────────────────────────────────────────
# # Request/Response models
# # ────────────────────────────────────────────────────────────────────────────────

# class GenerateRequest(BaseModel):
#     plan: Dict[str, Any]
#     prompt: Optional[str] = None          # optional; used to derive name
#     project_name: Optional[str] = None    # optional; if omitted we derive


# class GenerateResponse(BaseModel):
#     ok: bool
#     result: Dict[str, Any]


# router = APIRouter()


# @router.post("/generate", response_model=GenerateResponse)
# def generate(req: GenerateRequest) -> GenerateResponse:
#     """
#     Create a new project folder per request.
#     If project_name is omitted, we derive a clean folder name from plan/prompt.
#     """
#     project_name = req.project_name or derive_project_name(req.plan, req.prompt)
#     project_dir = WORKSPACE_ROOT / project_name

#     # Fail fast if for some reason it already exists (shouldn't, we ensure unique)
#     if project_dir.exists():
#         raise HTTPException(status_code=409, detail=f"Project '{project_name}' already exists")

#     # Create project directory
#     project_dir.mkdir(parents=True, exist_ok=False)

#     # ─────────────────────────────────────────────────────────────
#     # 🔧 Call your existing scaffolding logic here.
#     #    Keep whatever you already had; just pass project_dir.
#     #
#     # Examples (one of these likely matches your codebase):
#     #   from app.services.scaffold import scaffold_project
#     #   scaffold_project(project_root=project_dir, plan=req.plan)
#     #
#     # or
#     #   from app.codegen.generate import generate_project
#     #   generate_project(req.plan, str(project_dir))
#     #
#     # If you wrote files inline previously, keep that code and just use `project_dir`.
#     # ─────────────────────────────────────────────────────────────

#     return GenerateResponse(
#         ok=True,
#         result={
#             "project_name": project_name,
#             "project_root": str(project_dir),
#         },
#     )

# from __future__ import annotations

# import re
# from datetime import datetime
# from pathlib import Path
# from typing import Any, Dict, Optional

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel

# # ────────────────────────────────────────────────────────────────────────────────
# # Workspace root (…/backend/workspace)
# # ────────────────────────────────────────────────────────────────────────────────
# WORKSPACE_ROOT = Path(__file__).resolve().parents[2] / "workspace"
# WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)

# KNOWN_KEYS = {
#     "firebase": "firebase",
#     "stripe": "stripe",
#     "supabase": "supabase",
#     "postgres": "postgres",
#     "telnyx": "telnyx",
#     "twilio": "twilio",
#     "comet": "comet",
#     "comet_ml": "comet",
#     "openai": "openai",
#     "gemini": "gemini",
#     "gcp": "gcp",
#     "cloud run": "cloudrun",
# }

# def slugify(s: str) -> str:
#     s = s.lower()
#     s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
#     return re.sub(r"-{2,}", "-", s)

# def tokens_from_prompt(prompt: Optional[str]) -> list[str]:
#     if not prompt:
#         return []
#     p = prompt.lower()
#     found: list[str] = []
#     for k, token in KNOWN_KEYS.items():
#         if k in p:
#             found.append(token)
#     # dedupe preserving order
#     out, seen = [], set()
#     for t in found:
#         if t not in seen:
#             out.append(t)
#             seen.add(t)
#     return out

# def derive_project_name(plan: Dict[str, Any], prompt: Optional[str]) -> str:
#     """Build a unique, readable project name like firebase-stripe-app."""
#     names: list[str] = []
#     for itg in (plan.get("integrations") or []):
#         n = (itg.get("name") or "").strip()
#         if n:
#             names.append(slugify(n))
#     if not names:
#         names = tokens_from_prompt(prompt)
#     base = "-".join(sorted(set(names))) if names else "project"
#     if base in ("", "-", "project"):
#         base = f"project-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
#     base = slugify(base)[:48]
#     if not base.endswith("-app"):
#         base = f"{base}-app"
#     candidate = base
#     i = 2
#     while (WORKSPACE_ROOT / candidate).exists():
#         candidate = f"{base}-{i}"
#         i += 1
#     return candidate


# # ────────────────────────────────────────────────────────────────────────────────
# # Request/Response models
# # ────────────────────────────────────────────────────────────────────────────────
# class GenerateRequest(BaseModel):
#     plan: Dict[str, Any]
#     prompt: Optional[str] = None
#     project_name: Optional[str] = None

# class GenerateResponse(BaseModel):
#     ok: bool
#     result: Dict[str, Any]

# router = APIRouter()


# # ────────────────────────────────────────────────────────────────────────────────
# # File scaffolding helpers
# # ────────────────────────────────────────────────────────────────────────────────
# def write(path: Path, content: str):
#     path.parent.mkdir(parents=True, exist_ok=True)
#     path.write_text(content, encoding="utf-8")

# BASE_MAIN = """\
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI(title="Generated App")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], allow_credentials=True,
#     allow_methods=["*"], allow_headers=["*"],
# )

# @app.get("/")
# def root():
#     return {"ok": True, "service": "generated"}
# """

# DOCKERFILE = """\
# FROM python:3.11-slim
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY app ./app
# ENV PYTHONUNBUFFERED=1
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
# """

# README = """\
# # Generated App

# ## Run locally
# ```bash
# pip install -r requirements.txt
# uvicorn app.main:app --reload --port 8001
# """

# latestt 

# from __future__ import annotations
# from fastapi import APIRouter

# import re
# from datetime import datetime
# from pathlib import Path
# from typing import Any, Dict, Optional

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel

# print("[routers.generate] imported")  # should appear once at server startup

# router = APIRouter()

# @router.get("/__debug_generate")
# def __debug_generate():
#     return {"ok": True}
# # ────────────────────────────────────────────────────────────────────────────────
# # Workspace root (…/backend/workspace)
# # ────────────────────────────────────────────────────────────────────────────────
# WORKSPACE_ROOT = Path(__file__).resolve().parents[2] / "workspace"
# WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)

# # keywords we’ll try to extract from prompt for a nicer folder name
# KNOWN_KEYS = {
#     "firebase": "firebase",
#     "stripe": "stripe",
#     "supabase": "supabase",
#     "postgres": "postgres",
#     "telnyx": "telnyx",
#     "twilio": "twilio",
#     "comet": "comet",
#     "comet ml": "comet",
#     "comet_ml": "comet",
#     "openai": "openai",
#     "gemini": "gemini",
#     "gcp": "gcp",
#     "cloud run": "cloudrun",
# }

# def slugify(s: str) -> str:
#     s = s.lower()
#     s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
#     return re.sub(r"-{2,}", "-", s)

# def tokens_from_prompt(prompt: Optional[str]) -> list[str]:
#     if not prompt:
#         return []
#     p = prompt.lower()
#     found: list[str] = []
#     for k, token in KNOWN_KEYS.items():
#         if k in p:
#             found.append(token)
#     # dedupe preserving order
#     out, seen = [], set()
#     for t in found:
#         if t not in seen:
#             out.append(t); seen.add(t)
#     return out

# def derive_project_name(plan: Dict[str, Any], prompt: Optional[str]) -> str:
#     """
#     Build a unique, readable project name like 'stripe-firebase-app'.
#     Prefer integration names from the plan; fallback to prompt keywords.
#     """
#     names: list[str] = []
#     for itg in (plan.get("integrations") or []):
#         n = (itg.get("name") or "").strip()
#         if n:
#             names.append(slugify(n))

#     if not names:
#         names = tokens_from_prompt(prompt)

#     base = "-".join(sorted(set(names))) if names else "project"
#     if base in ("", "-", "project"):
#         base = f"project-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
#     base = slugify(base)[:48]
#     if not base.endswith("-app"):
#         base = f"{base}-app"

#     # ensure uniqueness
#     candidate = base
#     i = 2
#     while (WORKSPACE_ROOT / candidate).exists():
#         candidate = f"{base}-{i}"
#         i += 1
#     return candidate

# # ────────────────────────────────────────────────────────────────────────────────
# # Request/Response models
# # ────────────────────────────────────────────────────────────────────────────────
# class GenerateRequest(BaseModel):
#     plan: Dict[str, Any]
#     prompt: Optional[str] = None
#     project_name: Optional[str] = None

# class GenerateResponse(BaseModel):
#     ok: bool
#     result: Dict[str, Any]

# router = APIRouter()

# # ────────────────────────────────────────────────────────────────────────────────
# # Scaffolding helpers
# # ────────────────────────────────────────────────────────────────────────────────
# def write(path: Path, content: str):
#     path.parent.mkdir(parents=True, exist_ok=True)
#     path.write_text(content, encoding="utf-8")

# BASE_MAIN = """\
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI(title="Generated App")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], allow_credentials=True,
#     allow_methods=["*"], allow_headers=["*"],
# )

# @app.get("/")
# def root():
#     return {"ok": True, "service": "generated"}
# """

# DOCKERFILE = """\
# FROM python:3.11-slim
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY app ./app
# ENV PYTHONUNBUFFERED=1
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
# """

# README = """\
# # Generated App

# ## Run locally
# ```bash
# pip install -r requirements.txt
# uvicorn app.main:app --reload --port 8001
# """

# backend/app/routers/generate.py
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

print("[routers.generate] importing...")

# Workspace root (…/backend/workspace)
WORKSPACE_ROOT = Path(__file__).resolve().parents[2] / "workspace"
WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)

# Keywords we’ll try to extract from prompt for a nicer folder name
KNOWN_KEYS = {
    "firebase": "firebase",
    "stripe": "stripe",
    "supabase": "supabase",
    "postgres": "postgres",
    "telnyx": "telnyx",
    "twilio": "twilio",
    "comet": "comet",
    "comet ml": "comet",
    "comet_ml": "comet",
    "openai": "openai",
    "gemini": "gemini",
    "gcp": "gcp",
    "cloud run": "cloudrun",
}

def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-{2,}", "-", s)

def tokens_from_prompt(prompt: Optional[str]) -> list[str]:
    if not prompt:
        return []
    p = prompt.lower()
    found: list[str] = []
    for k, token in KNOWN_KEYS.items():
        if k in p:
            found.append(token)
    # dedupe preserving order
    out, seen = [], set()
    for t in found:
        if t not in seen:
            out.append(t)
            seen.add(t)
    return out

def derive_project_name(plan: Dict[str, Any], prompt: Optional[str]) -> str:
    """
    Build a unique, readable project name like 'stripe-firebase-app'.
    Prefer integration names from the plan; fallback to prompt keywords.
    """
    names: list[str] = []
    for itg in (plan.get("integrations") or []):
        n = (itg.get("name") or "").strip()
        if n:
            names.append(slugify(n))

    if not names:
        names = tokens_from_prompt(prompt)

    base = "-".join(sorted(set(names))) if names else "project"
    if base in ("", "-", "project"):
        base = f"project-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    base = slugify(base)[:48]
    if not base.endswith("-app"):
        base = f"{base}-app"

    # ensure uniqueness
    candidate = base
    i = 2
    while (WORKSPACE_ROOT / candidate).exists():
        candidate = f"{base}-{i}"
        i += 1
    return candidate

# ─────────────────────────────────────────────────────────────
# Request/Response models
# ─────────────────────────────────────────────────────────────
class GenerateRequest(BaseModel):
    plan: Dict[str, Any]
    prompt: Optional[str] = None
    project_name: Optional[str] = None

class GenerateResponse(BaseModel):
    ok: bool
    result: Dict[str, Any]

router = APIRouter()

# ─────────────────────────────────────────────────────────────
# Debug endpoint (keep while iterating)
# ─────────────────────────────────────────────────────────────
@router.get("/__debug_generate")
def __debug_generate():
    return {"ok": True}

# ─────────────────────────────────────────────────────────────
# Scaffolding helpers
# ─────────────────────────────────────────────────────────────
def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

REQS = """fastapi==0.115.0
uvicorn==0.30.6
"""

DOCKERFILE = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
"""

README = """# Generated App

Run locally
-----------
1) pip install -r requirements.txt
2) uvicorn app.main:app --reload --port 8001

Files
-----
- requirements.txt
- Dockerfile
- app/main.py
"""

MAIN_PY = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Generated App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"ok": True, "service": "generated"}
"""

def scaffold_project(plan: Dict[str, Any], project_dir: Path):
    """
    Write a minimal runnable FastAPI app into project_dir.
    """
    write(project_dir / "requirements.txt", REQS)
    write(project_dir / "Dockerfile", DOCKERFILE)
    write(project_dir / "README.md", README)
    write(project_dir / "app" / "main.py", MAIN_PY)

# ─────────────────────────────────────────────────────────────
# POST /generate
# ─────────────────────────────────────────────────────────────
@router.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest) -> GenerateResponse:
    # Decide the folder name (prefer explicit, otherwise derive)
    project_name = req.project_name or derive_project_name(req.plan, req.prompt)
    project_dir = WORKSPACE_ROOT / project_name

    if project_dir.exists():
        # Safety—your UI can handle 409 by letting user know it's taken
        raise HTTPException(status_code=409, detail=f"Project '{project_name}' already exists")

    project_dir.mkdir(parents=True, exist_ok=False)
    scaffold_project(req.plan, project_dir)

    return GenerateResponse(
        ok=True,
        result={"project_name": project_name, "project_root": str(project_dir)},
    )

print("[routers.generate] imported OK")

