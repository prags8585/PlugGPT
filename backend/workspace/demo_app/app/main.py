# from fastapi import FastAPI
# from dotenv import load_dotenv

# load_dotenv()

# app = FastAPI(title="demo_app")

# try:
#     from .routes import auth_routes
#     app.include_router(auth_routes.router)
# except Exception:
#     pass

# try:
#     from .routes import payment_routes
#     app.include_router(payment_routes.router)
# except Exception:
#     pass

# try:
#     from . import webhooks
# except Exception:
#     pass

# @app.get("/")
# def root():
#     return {"ok": True, "app": "demo_app"}

from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="demo_app")

# Include Firebase + Stripe routes if present
try:
    from .routes import auth_routes
    app.include_router(auth_routes.router)
except Exception:
    pass

try:
    from .routes import payment_routes
    app.include_router(payment_routes.router)
except Exception:
    pass

# ✅ Mount the webhook router (this was missing)
try:
    from .webhooks import router as webhooks_router
    app.include_router(webhooks_router)
except Exception:
    pass

@app.get("/")
def root():
    return {"ok": True, "app": "demo_app"}
