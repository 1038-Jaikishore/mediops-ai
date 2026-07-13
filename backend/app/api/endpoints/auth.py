from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
import jwt
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token
)
from app.api.deps import get_current_user, RoleChecker

router = APIRouter()

# --- Mock Users Database (with Pre-hashed passwords for security) ---
# Plaintext password is 'mediops_secure_pass_2026' for all users
MOCK_USERS_DB = {
    "admin": {
        "username": "admin",
        "hashed_password": get_password_hash("mediops_secure_pass_2026"),
        "roles": ["admin"]
    },
    "operator": {
        "username": "operator",
        "hashed_password": get_password_hash("mediops_secure_pass_2026"),
        "roles": ["operator"]
    },
    "viewer": {
        "username": "viewer",
        "hashed_password": get_password_hash("mediops_secure_pass_2026"),
        "roles": ["viewer"]
    }
}

# --- Pydantic Schemas ---

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserProfile(BaseModel):
    username: str
    roles: List[str]

# --- Endpoints ---

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    """
    Login endpoint. Verifies hashed credentials and returns JWT access and refresh tokens.
    """
    user = MOCK_USERS_DB.get(payload.username)
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(subject=user["username"], roles=user["roles"])
    refresh_token = create_refresh_token(subject=user["username"])

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=RefreshResponse)
async def refresh_token(payload: RefreshRequest):
    """
    Refresh token endpoint. Validates a refresh token and issues a new access token.
    """
    try:
        token_data = verify_token(payload.refresh_token)
        if token_data.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        
        username = token_data.get("sub")
        user = MOCK_USERS_DB.get(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
            
        # Issue a new access token
        access_token = create_access_token(subject=user["username"], roles=user["roles"])
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token signature has expired",
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate refresh token credentials",
        )


@router.get("/me", response_model=UserProfile)
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    """
    Profile endpoint. Decodes token to fetch authenticated user metadata.
    """
    return {
        "username": current_user["sub"],
        "roles": current_user["roles"]
    }


@router.get("/admin-only")
async def get_admin_restricted_resource(
    current_user: dict = Depends(RoleChecker(["admin"]))
):
    """
    Restricted endpoint requiring the 'admin' role.
    """
    return {"message": "Welcome Admin"}
