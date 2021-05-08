import pika
from worker_proxy_utils.rabbitmq_consumer_callback import RabbitmqConsumerCallback


class RabbitmqConsumer:
    def __init__(self, rabbit_host: str, rabbit_port: int, channel_name: str):
        self.rabbit_host = rabbit_host
        self.rabbit_port = rabbit_port
        self.channel_name = channel_name

    def consume(self, callback: RabbitmqConsumerCallback) -> bool:

        return True