import os
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def create_access_token(username: str) -> str:
    expiry_minutes = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRY_MINUTES"))
    secret_key = os.getenv("JWT_SECRET_KEY")
    algorithm = os.getenv("JWT_ALGORITHM")

    # 만료 시간 설정
    iat = datetime.now(timezone.utc)
    exp = iat + timedelta(minutes=expiry_minutes)

    # payload 생성
    payload = {
        "sub": username,  # 발행 대상
        "iat": iat,  # 발행 시간
        "exp": exp  # 만료 시간
    }

    # 토큰 생성
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def get_payload_from_access_token(token: str):
    secret_key = os.getenv("JWT_SECRET_KEY")
    algorithm = os.getenv("JWT_ALGORITHM")

    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
    except jwt.PyJWTError:
        return None
