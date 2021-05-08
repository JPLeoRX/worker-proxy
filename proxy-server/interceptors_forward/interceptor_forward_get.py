from injectable import injectable
from interceptors_forward.interceptor_forward import InterceptorForward
from fastapi import Request, Response
import requests
from worker_proxy_message_protocol import ProxyRequest


@injectable
class InterceptorForwardGet(InterceptorForward):
    def intercept(self, new_base_url: str, request: Request) -> Response:
        # Build new url
        old_url = str(request.url)
        old_base_url = str(request.base_url)
        old_path_url = old_url.replace(old_base_url, '')
        new_url = new_base_url + old_path_url

        # Make request
        forwarded_response = requests.get(new_url, headers=request.headers)
        print('InterceptorGet.intercept(): Forwarded from [' + old_url + '] to [' + new_url + ']')


        pr = ProxyRequest(
            request.method,
            str(request.url),
            str(request.base_url),
            request.headers,
            request.query_params,
            request.path_params,
            request.cookies,
            request.client
        )
        print(pr.json())

        # Return new response
        return Response(
            content=forwarded_response.content,
            status_code=forwarded_response.status_code,
            headers=forwarded_response.headers,
        )
