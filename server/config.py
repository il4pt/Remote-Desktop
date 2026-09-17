import os

class Config:
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8080))
    JWT_SECRET = os.getenv("JWT_SECRET", "remote-power-secure-secret-key-change-in-prod-2026")
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30  # 30 gün
    DEVICE_PING_TIMEOUT_SEC = 25  # Ajan 25 saniyeden fazla ping atmazsa offline sayılır
