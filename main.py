from fastapi import FastAPI, HTTPException, Query

from dotenv import load_dotenv
load_dotenv()
from shared.config.settings import settings

from pydantic import BaseModel, Field

from typing import List

app = FastAPI(
    title = settings.app_name,
    version = settings.api_version,
    debug = settings.debug
)


# Welcome message endpoint
class WelcomeResponse(BaseModel):
    """
    Response model for welcome message endpoint
    """
    message: str = Field(examples=["Welcome to Social Blog API"])
    version: str = Field(examples=["v1"])
    docs: str = Field(examples=["/docs"])

@app.get("/", response_model=WelcomeResponse)
def welcome_message() -> WelcomeResponse:
    """
    Root endopoint - API Welcome Message
    """
    return WelcomeResponse(
        message = "Welcome to Social Blog API",
        version = settings.api_version,
        docs = "/docs"
    )


# Health check
class HealthResponse(BaseModel):
    """
    Response model for health check endpoint
    """
    status: str = Field(examples=["ok"])
    app: str = Field(examples=["Social Blog"])

@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint for monitoring
    """
    return HealthResponse(
        status = "ok",
        app = settings.app_name
    )