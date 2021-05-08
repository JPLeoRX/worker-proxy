import json
import time
from injectable import injectable, autowired, Autowired
from fastapi import Request, Response
from worker_proxy_message_protocol import ProxyRequest, ProxyChannel, ProxyErrorResponse, ProxyResponse
from worker_proxy_utils import UtilsRabbitmq, UtilsId


@injectable
class Interceptor:
    @autowired
    def __init__(self, utils_id: Autowired(UtilsId), utils_rabbitmq: Autowired(UtilsRabbitmq)):
        self.utils_id = utils_id
        self.utils_rabbitmq = utils_rabbitmq

    def intercept(self, rabbit_host: str, rabbit_port: int, request: Request, sleep_interval_in_seconds: float = 0.2, receive_timeout_in_seconds: float =2.0) -> Response:
        # Track IDs
        id = self.utils_id.generate_uuid()
        request_id = 'request-' + id
        response_id = 'response-' + id

        # Build new request, and send it to rabbit
        proxy_request = self.build_proxy_request(request)
        self.utils_rabbitmq.send(rabbit_host, rabbit_port, request_id, str(proxy_request.json()))

        # Build new channel, and send it to rabbit
        proxy_channel = ProxyChannel(id, request_id, response_id)
        self.utils_rabbitmq.send(rabbit_host, rabbit_port, 'channels', str(proxy_channel.json()))

        # Hold a small pause, to allow client to catch-up and send the response
        time.sleep(sleep_interval_in_seconds)

        # Wait for response
        proxy_response_message = self.utils_rabbitmq.receive(rabbit_host, rabbit_port, response_id, timeout_in_seconds=receive_timeout_in_seconds)
        if proxy_response_message is None:
            error_response = ProxyErrorResponse(id, 'NO_RESPONSE_FROM_WORKER', 'The worker didn\'t provide any response within given time limit')
            return Response(content=str(error_response.json()), media_type="application/json", status_code=500)
        else:
            proxy_response = ProxyResponse.parse_obj(json.loads(proxy_response_message))
            return Response(content=proxy_response.content, status_code=proxy_response.status_code, headers=proxy_response.headers)

    def build_proxy_request(self, request: Request) -> ProxyRequest:
        return ProxyRequest(
            request.method,
            str(request.url),
            str(request.base_url),
            request.headers,
            request.query_params,
            request.path_params,
            request.cookies,
            await request.body(),
            request.client
        )
