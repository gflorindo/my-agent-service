from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
import os

app: FastAPI = get_fast_api_app(
    # Scan account_discovery_agent/ folder for agents to serve.
    agents_dir=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "account_discovery_agent"
    ),
    session_service_uri="sqlite:///./sessions.db",
    allow_origins=["*"],
    web=True,
)
