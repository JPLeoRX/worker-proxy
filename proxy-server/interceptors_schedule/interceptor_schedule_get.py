from injectable import injectable, autowired, Autowired
from interceptors_schedule.interceptor_schedule import InterceptorSchedule
from fastapi import Request, Response
from worker_proxy_message_protocol import ProxyRequest, ProxyChannel, ProxyErrorResponse
from worker_proxy_utils import UtilsRabbitmq, UtilsId


@injectable
class InterceptorScheduleGet(InterceptorSchedule):
    @autowired
    def __init__(self, utils_id: Autowired(UtilsId), utils_rabbitmq: Autowired(UtilsRabbitmq)):
        self.utils_id = utils_id
        self.utils_rabbitmq = utils_rabbitmq

    def intercept(self, rabbit_host: str, rabbit_port: int, request: Request) -> Response:
        # Track IDs
        id = self.utils_id.generate_uuid()
        request_channel = 'request-' + id
        response_channel = 'response-' + id

        # Build new request, and send it to rabbit
        proxy_request = ProxyRequest(
            request.method,
            str(request.url),
            str(request.base_url),
            request.headers,
            request.query_params,
            request.path_params,
            request.cookies,
            request.client
        )
        proxy_request_json_str = str(proxy_request.json())
        self.utils_rabbitmq.send(rabbit_host, rabbit_port, request_channel, proxy_request_json_str)

        # Build new channel, and send it to rabbit
        proxy_channel = ProxyChannel(id, request_channel, response_channel)
        proxy_channel_json_str = str(proxy_channel.json())
        self.utils_rabbitmq.send(rabbit_host, rabbit_port, 'channels', proxy_channel_json_str)

        # Wait for response
        proxy_response = self.utils_rabbitmq.receive(rabbit_host, rabbit_port, response_channel, timeout_in_seconds=1.0)
        if proxy_response is None:
            error_response = ProxyErrorResponse(id, 'NO_RESPONSE_FROM_WORKER', 'The worker didn\'t provide any response within given time limit')
            return Response(content=str(error_response.json()), media_type="application/json", status_code=500)
        else:
            return Response(status_code=200)


