# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import Optional, Dict, Any
# from ..services.planner import plan_integrations

# router = APIRouter()

# class PlanRequest(BaseModel):
#     prompt: str
#     model: Optional[str] = None  # "gemini" | "openai" | None

# @router.post("/plan")
# def plan_endpoint(req: PlanRequest):
#     try:
#         return plan_integrations(req.prompt, model=req.model)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Map prompt keywords -> integration "names" your generator/templates understand
# Add more rows here anytime you support a new integration.
KEYWORD_TO_INTEGRATION = [
    # auth/payments
    (r"\bfirebase\b",           "firebase_auth"),
    (r"\bstripe\b",             "stripe_payments"),

    # telco / sms
    (r"\btelnyx\b",             "telnyx_sms"),
    (r"\btwilio\b",             "twilio_sms"),

    # ml / tracking
    (r"\bcomet(\s*ml)?\b",      "comet_ml"),
    (r"\bwandb\b|\bweights\b",  "wandb_tracking"),

    # db / infra examples
    (r"\bpostgres(ql)?\b",      "postgres_db"),
    (r"\bsupabase\b",           "supabase_db"),
]

# Very light normalization
def detect_integrations(prompt: str) -> List[str]:
    found: List[str] = []
    p = prompt.lower()
    for pattern, integration in KEYWORD_TO_INTEGRATION:
        if re.search(pattern, p):
            found.append(integration)
    # De-dup while preserving order
    seen = set()
    unique = []
    for x in found:
        if x not in seen:
            unique.append(x); seen.add(x)
    return unique

class PlanRequest(BaseModel):
    prompt: str

class PlanResponse(BaseModel):
    prompt: str
    integrations: List[Dict[str, Any]]
    deployment: Dict[str, str]

@router.post("/plan", response_model=PlanResponse)
def plan(req: PlanRequest) -> PlanResponse:
    """
    Simple keyword-based planner.
    - Scans the prompt for known keywords
    - Emits integration names your generator understands
    - Supplies a default deployment target
    """
    integration_ids = detect_integrations(req.prompt)

    integrations = [{"name": name} for name in integration_ids]

    # Default deployment; tweak if your UI lets users choose others.
    deployment = {"platform": "local_dev", "iac": "none"}

    # If nothing matched at all, keep it empty but still return a valid plan
    return PlanResponse(
        prompt=req.prompt,
        integrations=integrations,
        deployment=deployment,
    )
