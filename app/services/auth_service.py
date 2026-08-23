import datetime
import hashlib
import hmac
import os
import jwt
from passlib.context import CryptContext
from app.config import settings
from app.schemas.auth import TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # Fallback to salted SHA-256 if passlib bcrypt fails on specific environments
        salt = hashed_password[:32] if len(hashed_password) > 64 else ""
        expected = hashed_password[32:] if salt else hashed_password
        test_hash = hashlib.sha256((salt + plain_password).encode()).hexdigest()
        return hmac.compare_digest(test_hash, expected)

def get_password_hash(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except Exception:
        salt = os.urandom(16).hex()
        hash_val = hashlib.sha256((salt + password).encode()).hexdigest()
        return salt + hash_val

def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> TokenPayload | None:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        is_admin: bool = payload.get("is_admin", False)
        if username is None:
            return None
        return TokenPayload(sub=username, exp=payload.get("exp"), is_admin=is_admin)
    except jwt.PyJWTError:
        return None
