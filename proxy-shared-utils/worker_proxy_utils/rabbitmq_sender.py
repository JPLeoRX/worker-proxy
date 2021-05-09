import pika
from worker_proxy_message_protocol import RabbitmqConfig


class RabbitmqSender:
    def __init__(self, rabbitmq_config: RabbitmqConfig, channel_name: str):
        self.rabbitmq_config = rabbitmq_config
        self.channel_name = channel_name

    def send(self, message: str) -> bool:
        credentials = pika.PlainCredentials(self.rabbitmq_config.username, self.rabbitmq_config.password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_config.host, port=self.rabbitmq_config.port, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue=self.channel_name)
        channel.basic_publish(exchange='', routing_key=self.channel_name, body=message)
        connection.close()
        return True
