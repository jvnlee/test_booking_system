import os
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    expires_in_minutes = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_IN"))
    secret_key = os.getenv("JWT_SECRET_KEY")
    algorithm = os.getenv("JWT_ALGORITHM")

    # 만료 시간 설정
    exp = datetime.now() + timedelta(minutes=expires_in_minutes)

    # payload 생성
    to_encode = data.copy()
    to_encode.update({
        "exp": exp,  # 만료 시간
        "iat": datetime.now(),  # 토큰 발행 시간
    })

    # 토큰 생성
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_access_token(token: str):
    secret_key = os.getenv("JWT_SECRET_KEY")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
