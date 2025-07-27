from functools import wraps
from flask import request, jsonify
from sierra_madre_core.errors import HTTPError
from sierra_madre_core.schemas import ValidationError
from sierra_madre_auth.config import AuthConfig

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"


def generate_jwt(user_id: str, config: AuthConfig) -> str:
    payload = {
        "id_user": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "exp": datetime.utcnow() + timedelta(minutes=config.token_expiration_time_minutes)  # o el tiempo que quieras
    }
    token = jwt.encode(payload, config.password_hash_key, algorithm=config.algorithm)
    return token

def decode_jwt(token: str, config: AuthConfig) -> dict:
    try:
        payload = jwt.decode(token, config.password_hash_key, algorithms=[config.algorithm])
        return payload
    except ExpiredSignatureError:
        raise HTTPError("Token expired", 401)
    except InvalidTokenError:
        raise HTTPError("Invalid token", 401)



def validate_token():
    token = request.headers.get("Authorization")
    token = token.split(" ")
    if token[0] != "Bearer":
        raise HTTPError("Invalid token", 401)
    token = token[1]
    return decode_jwt(token)["id_user"]