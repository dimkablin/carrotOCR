"""Middleware"""
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class BackendMiddleware(BaseHTTPMiddleware):
    """Middleware for carrotOCR backend."""
    ERRORS = (RuntimeError, TypeError, Exception)

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)

            return response

        except self.ERRORS as error:
            print(error)

    def __str__(self):
        return ""
