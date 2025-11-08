from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import plan, generate, deploy, secrets, health

app = FastAPI(title="PlugGPT", version="0.4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(plan.router, prefix="/api")
app.include_router(generate.router, prefix="/api")
app.include_router(deploy.router, prefix="/api")
app.include_router(secrets.router, prefix="/api")

@app.get("/")
def root():
    return {"ok": True, "service": "PlugGPT", "version": "0.4.0"}
