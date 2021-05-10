import json
from injectable import injectable, autowired, Autowired
from worker_proxy_message_protocol import ProxyChannel, ProxyRequest
from worker_proxy_utils import UtilsEnv, UtilsRabbitmq
from request_forwarder import RequestForwarder


@injectable
class ChannelProcessor():
    @autowired
    def __init__(self, utils_env: Autowired(UtilsEnv), utils_rabbitmq: Autowired(UtilsRabbitmq), request_forwarder: Autowired(RequestForwarder)):
        self.utils_env = utils_env
        self.utils_rabbitmq = utils_rabbitmq
        self.request_forwarder = request_forwarder

    def process(self, proxy_channel: ProxyChannel):
        # Keep rabbitmq config
        rabbitmq_config = self.utils_env.get_rabbitmq_config()

        # Read new proxy request
        proxy_request_message = self.utils_rabbitmq.receive(rabbitmq_config, proxy_channel.request_id)
        proxy_request = ProxyRequest.parse_obj(json.loads(proxy_request_message))
        print('ChannelProcessor.process(): Parsed proxy request ' + str(proxy_request))

        # Forward and build response
        proxy_response = self.request_forwarder.forward(proxy_channel.id, proxy_request)
        print('ChannelProcessor.process(): Formed proxy response ' + str(proxy_response))

        # Send response
        self.utils_rabbitmq.send(rabbitmq_config, proxy_channel.response_id, str(proxy_response.json()))
