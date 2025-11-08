# Stripe webhook receiver
from fastapi import APIRouter, Request, Header, HTTPException
import os

router = APIRouter(tags=["webhooks"])

@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        import stripe
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        if endpoint_secret and stripe_signature:
            event = stripe.Webhook.construct_event(
                payload=payload, sig_header=stripe_signature, secret=endpoint_secret
            )
            t = event.get("type")
        else:
            t = "unverified"
        return {"received": True, "event_type": t, "length": len(payload)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))