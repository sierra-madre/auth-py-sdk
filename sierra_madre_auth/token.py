from sierra_madre_core.errors import HTTPError

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta


def generate_jwt(user_id: str, secret_key: str, algorithm: str, expiration_time_minutes: int) -> str:
    payload = {
        "id_user": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "exp": datetime.utcnow() + timedelta(minutes=expiration_time_minutes)  
    }
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def decode_jwt(token: str, secret_key: str, algorithm: str) -> dict:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except ExpiredSignatureError:
        raise HTTPError("Token expired", 401)
    except InvalidTokenError:
        raise HTTPError("Invalid token", 401)



