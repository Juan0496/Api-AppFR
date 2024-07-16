from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import credentials, initialize_app, auth
from pydantic import BaseModel
import time

class TokenRequest(BaseModel):
    id_token: str

security = HTTPBearer()

def create_session_token(request: TokenRequest):
    try:
        # Duración de la sesión en milisegundos (14 días)
        expires_in = 60 * 60 * 24 * 14 * 1000
        # Crea el token de sesión
        session_cookie = auth.create_session_cookie(request.id_token, {'expiresIn': expires_in})
        return {"session_token": session_cookie}
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid ID token")

def verify_session_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        decoded_token = auth.verify_session_cookie(credentials.credentials, check_revoked=True)
        return decoded_token
    except auth.InvalidSessionCookieError:
        raise HTTPException(status_code=401, detail="Invalid session token")