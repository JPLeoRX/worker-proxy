import pika


class RabbitmqSender:
    def __init__(self, rabbit_host: str, rabbit_port: int, channel_name: str):
        self.rabbit_host = rabbit_host
        self.rabbit_port = rabbit_port
        self.channel_name = channel_name

    def send(self, message: str) -> bool:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbit_host, port=self.rabbit_port))
        channel = connection.channel()
        channel.queue_declare(queue=self.channel_name)
        channel.basic_publish(exchange='', routing_key=self.channel_name, body=message)
        connection.close()
        return True
