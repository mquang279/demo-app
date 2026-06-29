from prometheus_client import Counter, Histogram, Info

from .config import settings


HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "route", "status_code"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "route", "status_code"],
)

HTTP_ERRORS_TOTAL = Counter(
    "http_errors_total",
    "Total number of HTTP 5xx responses",
    ["method", "route", "status_code"],
)

APP_INFO = Info("app", "Application build information")
APP_INFO.info({"version": settings.app_version, "service": settings.service_name})
