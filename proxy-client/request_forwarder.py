import requests
from injectable import injectable, autowired, Autowired
from worker_proxy_message_protocol import ProxyResponse, ProxyRequest, ProxyErrorResponse
from worker_proxy_utils import UtilsEnv


@injectable
class RequestForwarder:
    @autowired
    def __init__(self, utils_env: Autowired(UtilsEnv)):
        self.utils_env = utils_env

    def forward(self, id: str, proxy_request: ProxyRequest) -> ProxyResponse:
        # Build new url
        new_base_url = self.utils_env.worker_proxy_client_proxied_base_url
        old_url = str(proxy_request.url)
        old_base_url = str(proxy_request.base_url)
        old_path_url = old_url.replace(old_base_url, '')
        new_url = new_base_url + old_path_url

        # Try to make request
        try:
            forwarded_response = None
            if proxy_request.method == 'GET':
                forwarded_response = requests.get(new_url, headers=proxy_request.headers)
            elif proxy_request.method == 'POST':
                forwarded_response = requests.post(new_url, data=proxy_request.body, headers=proxy_request.headers)
            elif proxy_request.method == 'PUT':
                forwarded_response = requests.put(new_url, data=proxy_request.body, headers=proxy_request.headers)
            elif proxy_request.method == 'DELETE':
                forwarded_response = requests.delete(new_url, headers=proxy_request.headers)
            else:
                raise RuntimeError("Unsupported method: " + proxy_request.method)
            print('RequestForwarder.forward(): Forwarded from [' + old_url + '] to [' + new_url + ']')
            return ProxyResponse(forwarded_response.content, forwarded_response.status_code, forwarded_response.headers)

        # If we failed to connect to the proxied service
        except requests.exceptions.ConnectionError:
            proxy_error_response = ProxyErrorResponse(id, 'NO_CONNECTION_TO_WORKER', 'The worker\'s proxy client has received and tried to process request, but failed to establish connection to proxied service url [' + new_url + ']')
            print('RequestForwarder.forward(): Failed to forward from [' + old_url + '] to [' + new_url + ']')
            return ProxyResponse(str(proxy_error_response.json()), 500, {"Content-Type": "application/json"})
