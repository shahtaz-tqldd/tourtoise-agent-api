import jwt
from typing import Dict
from datetime import datetime, timedelta, timezone

from app.core.config import get_settings
settings = get_settings()


JWT_SECRET = settings.jwt_secret_key


def create_tokens(user_id: str) -> Dict[str, str]:
    now = datetime.now(timezone.utc)

    access_payload = {
        "user_id": user_id,
        "type": "access",
        "exp": now + timedelta(seconds=settings.access_token_expire_minutes * 60),
        "iat": now,
    }
    refresh_payload = {
        "user_id": user_id,
        "type": "refresh",
        "exp": now + timedelta(days=settings.refresh_token_expire_days),
        "iat": now,
    }

    access_token = jwt.encode(access_payload, JWT_SECRET, algorithm=settings.jwt_algorithm)
    refresh_token = jwt.encode(refresh_payload, JWT_SECRET, algorithm=settings.jwt_algorithm)

    return {"access_token": access_token, "refresh_token": refresh_token}


def decode_jwt(token: str) -> dict | None:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[settings.jwt_algorithm])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None