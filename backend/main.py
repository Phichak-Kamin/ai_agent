"""FastAPI entry point for the smart factory orchestrator."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers.factory import router as factory_router
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Smart Factory Orchestrator", version="0.1.0")
app.include_router(factory_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"],
)


@app.get("/")
async def healthcheck():
    return {
        "factory": settings.factory_name,
        "message": "Smart factory orchestrator is online",
    }
