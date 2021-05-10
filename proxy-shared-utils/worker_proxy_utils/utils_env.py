import os
from injectable import injectable
from worker_proxy_message_protocol import RabbitmqConfig


@injectable
class UtilsEnv:
    def __init__(self):
        self.worker_proxy_rabbitmq_host = ''
        self.worker_proxy_rabbitmq_port = -1
        self.worker_proxy_rabbitmq_username = ''
        self.worker_proxy_rabbitmq_password = ''
        self.worker_proxy_client_proxied_base_url = ''
        self.__reload()

    def __reload(self):
        if 'WORKER_PROXY_RABBITMQ_HOST' in os.environ:
            self.worker_proxy_rabbitmq_host = os.environ['WORKER_PROXY_RABBITMQ_HOST']
        else:
            print('UtilsEnv.__reload(): Warning! WORKER_PROXY_RABBITMQ_HOST not found')

        if 'WORKER_PROXY_RABBITMQ_PORT' in os.environ:
            self.worker_proxy_rabbitmq_port = int(os.environ['WORKER_PROXY_RABBITMQ_PORT'])
        else:
            print('UtilsEnv.__reload(): Warning! WORKER_PROXY_RABBITMQ_PORT not found')

        if 'WORKER_PROXY_RABBITMQ_USERNAME' in os.environ:
            self.worker_proxy_rabbitmq_username = os.environ['WORKER_PROXY_RABBITMQ_USERNAME']
        else:
            print('UtilsEnv.__reload(): Warning! WORKER_PROXY_RABBITMQ_USERNAME not found')

        if 'WORKER_PROXY_RABBITMQ_PASSWORD' in os.environ:
            self.worker_proxy_rabbitmq_password = os.environ['WORKER_PROXY_RABBITMQ_PASSWORD']
        else:
            print('UtilsEnv.__reload(): Warning! WORKER_PROXY_RABBITMQ_PASSWORD not found')

        if 'WORKER_PROXY_CLIENT_PROXIED_BASE_URL' in os.environ:
            self.worker_proxy_client_proxied_base_url = os.environ['WORKER_PROXY_CLIENT_PROXIED_BASE_URL']
        else:
            print('UtilsEnv.__reload(): Warning! WORKER_PROXY_CLIENT_PROXIED_BASE_URL not found')

    def get_rabbitmq_config(self) -> RabbitmqConfig:
        return RabbitmqConfig(self.worker_proxy_rabbitmq_host, self.worker_proxy_rabbitmq_port, self.worker_proxy_rabbitmq_username, self.worker_proxy_rabbitmq_password)
