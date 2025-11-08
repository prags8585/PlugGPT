# Offline-friendly mock planner. Swap with Gemini/OpenAI as needed.
import re
from typing import Dict, Any

def _has(term: str, text: str) -> bool:
    return re.search(rf"\b{re.escape(term)}\b", text, flags=re.IGNORECASE) is not None

def plan_integrations(prompt: str, model: str | None = None) -> Dict[str, Any]:
    integrations = []
    if any(_has(t, prompt) for t in ["firebase", "auth", "login"]):
        integrations.append({"name": "firebase_auth"})
    if any(_has(t, prompt) for t in ["stripe", "payment", "checkout", "subscription"]):
        integrations.append({"name": "stripe_payments"})
    deployment = {"platform": "local_dev", "iac": "none"}
    if any(_has(t, prompt) for t in ["gcp", "cloud run", "deploy"]):
        deployment = {"platform": "gcp_cloud_run", "iac": "terraform"}
    return {"prompt": prompt, "integrations": integrations, "deployment": deployment}
