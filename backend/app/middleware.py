import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from .logger import log_request
from .metrics import (
    HTTP_ERRORS_TOTAL,
    HTTP_REQUEST_DURATION_SECONDS,
    HTTP_REQUESTS_TOTAL,
)


class ObservabilityMiddleware(BaseHTTPMiddleware):
    """Add request correlation, access logs, and Prometheus HTTP metrics."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        start_time = time.perf_counter()
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers["x-request-id"] = request_id
            return response
        finally:
            duration_seconds = time.perf_counter() - start_time
            route = request.scope.get("route")
            route_path = getattr(route, "path", request.url.path)
            method = request.method
            status = str(status_code)

            # Excluding the scrape endpoint keeps monitoring traffic out of app metrics.
            if request.url.path != "/metrics":
                labels = {"method": method, "route": route_path, "status_code": status}
                HTTP_REQUESTS_TOTAL.labels(**labels).inc()
                HTTP_REQUEST_DURATION_SECONDS.labels(**labels).observe(duration_seconds)
                if status_code >= 500:
                    HTTP_ERRORS_TOTAL.labels(**labels).inc()

            log_request(
                method=method,
                path=request.url.path,
                status_code=status_code,
                duration_ms=duration_seconds * 1000,
                request_id=request_id,
            )
