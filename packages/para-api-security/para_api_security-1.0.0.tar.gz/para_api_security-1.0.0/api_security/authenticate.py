import base64
import json

import requests
from fastapi import APIRouter, Body, HTTPException, Request
from pydantic import BaseModel

from config import settings

# Initialize router
authenticate_router = APIRouter()

# Keycloak configuration
KEYCLOAK_CLIENT_ID = settings.KEYCLOAK_CLIENT_ID
KEYCLOAK_MIDDLEWARE_SECRET = settings.KEYCLOAK_MIDDLEWARE_SECRET
KEYCLOAK_SERVER = settings.KEYCLOAK_BASE_URL
REALM = "para-smartVillage"


class AuthResponse(BaseModel):
    access_token: str
    token_type: str


@authenticate_router.post("/authenticate", response_model=AuthResponse)
def authenticate(
        request: Request,
        client_id: str = Body(...),
        client_secret: str = Body(...)
):
    # Get the base URL dynamically
    base_url = f"{request.url.scheme}://{request.url.hostname}:{request.url.port}"
    send_otp_url = f"{base_url}/send-otp"  # Set the URL dynamically

    # Step 1: Validate para-application client via Keycloak
    client_validation_url = f"{KEYCLOAK_SERVER}/realms/{REALM}/protocol/openid-connect/token"
    validation_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    client_validation_response = requests.post(client_validation_url, data=validation_data)

    if client_validation_response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid client credentials")

    # Step 2: Extract the access token from the response
    access_token = client_validation_response.json().get("access_token")
    token_type = client_validation_response.json().get("token_type")

    if not access_token:
        raise HTTPException(status_code=400, detail="Failed to obtain access token")

    token_parts = access_token.split(".")
    payload = json.loads(base64.urlsafe_b64decode(token_parts[1] + "==").decode())

    # Step 3: Return the access token
    return AuthResponse(access_token=access_token, token_type=token_type)

