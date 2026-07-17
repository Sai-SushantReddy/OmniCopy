from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import SessionLocal
from app.core.redis import redis_client

sysrouter = APIRouter(
    prefix="/system",
    tags=["System"]
)


@sysrouter.get("/health")
def health():
    return {"status": "healthy"}


@sysrouter.get("/ready")
def ready():
    db = SessionLocal()

    try:
        db.execute(text("SELECT 1"))
        redis_client.ping()

        return {"status": "ready"}

    except Exception:
        return {"status": "not ready"}

    finally:
        db.close()