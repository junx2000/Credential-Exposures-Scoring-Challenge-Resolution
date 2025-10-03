import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

logger = logging.getLogger("scoring_app")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log de la request
        body = await request.body()
        logger.info(
                    "Request: %s %s - Body: %s",
                    request.method,
                    request.url,
                    body.decode("utf-8") if body else "empty"
                )
        
        response = await call_next(request)

        # Log de la response
        process_time = time.time() - start_time
        logger.info(
            "Response: %s %s - Status: %d - Time: %.3fs",
            request.method,
            request.url,
            response.status_code,
            process_time
        )

        return response
