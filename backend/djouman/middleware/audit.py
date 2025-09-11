import time
from django.utils.deprecation import MiddlewareMixin
import uuid
import logging

logger = logging.getLogger(__name__)

class AuditMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._trace_id = uuid.uuid4().hex
        request._start_time = time.time()

    def process_response(self, request, response):
        try:
            duration_ms = int((time.time() - getattr(request, "_start_time", time.time())) * 1000)
            trace_id = getattr(request, "_trace_id", "-")
            logger.info(
                "audit",
                extra={
                    "trace_id": trace_id,
                    "path": getattr(request, "path", ""),
                    "method": getattr(request, "method", ""),
                    "status_code": getattr(response, "status_code", 0),
                    "duration_ms": duration_ms,
                },
            )
            response["X-Trace-Id"] = trace_id
        except Exception:
            pass
        return response
