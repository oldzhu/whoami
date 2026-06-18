"""Authentication API endpoints."""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from ..core.auth import get_auth
from ..middleware import auth_required

router = APIRouter(prefix="/api/auth", tags=["auth"])


class SetupRequest(BaseModel):
    username: str = Field(min_length=2, max_length=64)
    password: str = Field(min_length=4, max_length=128)


class LoginRequest(BaseModel):
    username: str
    password: str


@router.get("/status")
async def auth_status():
    auth = get_auth()
    return {"setup": auth.is_setup()}


@router.post("/setup")
async def auth_setup(body: SetupRequest):
    auth = get_auth()
    if auth.is_setup():
        raise HTTPException(status_code=400, detail="Authentication already set up")
    auth.setup(body.username, body.password)
    token = auth.create_session(body.username)
    return {"token": token, "username": body.username}


@router.post("/login")
async def auth_login(body: LoginRequest):
    auth = get_auth()
    if not auth.is_setup():
        raise HTTPException(status_code=400, detail="Authentication not set up yet")
    if not auth.verify(body.username, body.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = auth.create_session(body.username)
    return {"token": token, "username": body.username}


class ResetRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=4, max_length=128)


@router.post("/reset")
async def auth_reset(body: ResetRequest, username: str = Depends(auth_required)):
    auth = get_auth()
    if not auth.verify(username, body.current_password):
        raise HTTPException(status_code=401, detail="Current password is incorrect")
    auth.reset_password(username, body.new_password)
    return {"status": "password_updated"}
