from fastapi import APIRouter

status_router = APIRouter()


@status_router.get("/")
def status():
    return {
        "ok": True,
        "version": "0.2.0"
    }
