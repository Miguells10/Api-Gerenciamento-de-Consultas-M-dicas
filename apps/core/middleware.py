import logging
import time

logger = logging.getLogger("apps.access")

class AccessLogMiddleware:
    """
    Middleware to log every request made to the API.
    Logs method, path, status code, user, and duration.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time
        user = request.user if request.user.is_authenticated else "Anonymous"

        log_data = {
            "method": request.method,
            "path": request.get_full_path(),
            "status_code": response.status_code,
            "user": str(user),
            "duration": f"{duration:.3f}s",
            "ip": self.get_client_ip(request),
        }

        logger.info(
            f"{log_data['method']} {log_data['path']} - {log_data['status_code']} "
            f"({log_data['user']}) from {log_data['ip']} took {log_data['duration']}"
        )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
