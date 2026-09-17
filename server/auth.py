from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import secrets
import hashlib
from config import Config

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

def generate_pairing_code() -> str:
    """Mobil uygulama ile PC Ajanını 6 haneli güvenli PIN veya QR ile eşleştirmek için kod üretir"""
    return secrets.token_hex(3).upper()  # Örn: A1B2C3

def generate_device_token() -> str:
    """Cihaz için kalıcı güvenli API anahtarı"""
    return "rp_dev_" + secrets.token_urlsafe(32)
