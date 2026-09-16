from fastapi import FastAPI

from app.routers import auth
from app.routers import tasks


app = FastAPI(
    title="FastAPI Firebase Task Manager",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "FastAPI Firebase API"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


app.include_router(auth.router)
app.include_router(tasks.router)