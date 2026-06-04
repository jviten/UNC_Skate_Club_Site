from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import spots

app = FastAPI(title="UNC Skate Club spot map")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(spots.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
