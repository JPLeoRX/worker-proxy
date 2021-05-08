from fastapi import Request, Response


class InterceptorSchedule:
    def intercept(self, rabbit_host: str, rabbit_port: str, request: Request) -> Response:
        pass
