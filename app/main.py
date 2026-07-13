from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.contents import router as contents_router

app = FastAPI(
    title="OmniCopy API",
    version="1.0.0"
)

app.include_router(
    auth_router,
    prefix="/api/v1"
)

app.include_router(
    users_router,
    prefix="/api/v1"
)

app.include_router(
    contents_router,
    prefix="/api/v1"
)



@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }