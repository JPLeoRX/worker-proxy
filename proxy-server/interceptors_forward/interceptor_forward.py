from fastapi import Request, Response


class InterceptorForward:
    def intercept(self, new_base_url: str, request: Request) -> Response:
        pass
