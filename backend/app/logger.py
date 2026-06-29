import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any

from .config import settings


logger = logging.getLogger(settings.service_name)
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)


def log_request(
    *,
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    request_id: str,
) -> None:
    """Write one structured JSON log entry for an HTTP request."""
    level = "error" if status_code >= 500 else "info"
    entry: dict[str, Any] = {
        "level": level,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": settings.service_name,
        "version": settings.app_version,
        "method": method,
        "path": path,
        "status_code": status_code,
        "duration_ms": round(duration_ms, 2),
        "request_id": request_id,
    }
    logger.log(logging.ERROR if status_code >= 500 else logging.INFO, json.dumps(entry))
