from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from .config import settings
from .middleware import ObservabilityMiddleware


app = FastAPI(title="CI/CD Observability Demo", version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ObservabilityMiddleware)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.service_name,
        "version": settings.app_version,
    }


@app.get("/api/version")
async def version() -> dict[str, str]:
    return {"version": settings.app_version}


@app.get("/api/message")
async def message() -> dict[str, str]:
    return {
        "message": "Hello from CI/CD Observability Demo",
        "version": settings.app_version,
    }


@app.get("/api/items")
async def items() -> list[dict[str, int | str]]:
    return [
        {"id": 1, "name": "Continuous Integration"},
        {"id": 2, "name": "Continuous Delivery"},
        {"id": 3, "name": "Cloud Observability"},
    ]


@app.get("/api/error")
async def simulated_error() -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"error": "Simulated internal server error"},
    )


@app.get("/metrics", include_in_schema=False)
async def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
