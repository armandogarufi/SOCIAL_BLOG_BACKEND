from fastapi import FastAPI

from dotenv import load_dotenv
load_dotenv()
from shared.config.settings import settings
from typing import Dict

app = FastAPI(
    title = settings.app_name,
    version = settings.api_version,
    debug = settings.debug
)


@app.get("/")
def welcome_message() -> Dict[str, str]:
    """
    Root endopoint - API Welcome Message
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.api_version,
        "docs": "/docs"
    }

@app.get("/health")
def health_check() -> Dict[str, str]:
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "ok",
        "app": settings.app_name
    }