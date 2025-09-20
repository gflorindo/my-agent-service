from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
import os

app: FastAPI = get_fast_api_app(
    agents_dir=os.path.dirname(os.path.abspath(__file__)),
    session_service_uri="sqlite:///./sessions.db",
    allow_origins=["*"],
    web=True
)
