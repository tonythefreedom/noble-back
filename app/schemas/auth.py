from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginResponse(BaseModel):
    success: bool = True
    message: str
    data: dict

class LogoutResponse(BaseModel):
    success: bool = True
    message: str

class VerifyResponse(BaseModel):
    success: bool = True
    data: dict
