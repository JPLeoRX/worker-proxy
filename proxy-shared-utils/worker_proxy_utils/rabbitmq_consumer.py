import pika
from worker_proxy_utils.rabbitmq_consumer_callback import RabbitmqConsumerCallback


class RabbitmqConsumer:
    def __init__(self, rabbit_host: str, rabbit_port: int, channel_name: str):
        self.rabbit_host = rabbit_host
        self.rabbit_port = rabbit_port
        self.channel_name = channel_name

    def consume(self, callback: RabbitmqConsumerCallback) -> bool:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbit_host, port=self.rabbit_port))
        channel = connection.channel()
        channel.queue_declare(queue=self.channel_name)
        channel.basic_consume(queue=self.channel_name, auto_ack=False, on_message_callback=callback.callback)
        connection.process_data_events()
        return True