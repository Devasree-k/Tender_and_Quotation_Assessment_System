import secrets
from hashlib import sha256
from datetime import UTC, datetime, timedelta
from typing import Any 

import jwt
from pwdlib import PasswordHash 

from app.core.config import (
    ACCESS_TOKEN_EXPIRATION_TIME,
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
)

Password_hash = PasswordHash.recommended()

def hash_password(password:str) ->str :
    return Password_hash.hash(password)

def verify_password(plain_password: str , hashed_password: str) -> bool:
    return Password_hash.verify(plain_password, hashed_password)

def create_access_token(user_id: int , role: str) -> str:
    now = datetime.now(UTC)
    payload = dict[str, Any] = {
        "sub" : str(user_id),
        "role" : role,
        "type" : "access",
        "iat" : now,
        "exp" : now + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_TIME),

    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm= JWT_ALGORITHM)

def decode_token(token:str )->dict[str, Any]:
    return jwt.decode(
        token,
        JWT_SECRET_KEY,
        algorithm=[JWT_ALGORITHM],
        options={
            "require" : ["sub", "exp", "type", "iat", "role"]
        },
    )

def create_refresh_token()->str:
    return secrets.token_urlsafe(48)

def hash_refresh_token(token:str )->str:
    return sha256(token.encode("utf-8")).hexdigest()



