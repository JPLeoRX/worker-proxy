import threading
import pika


class Callback:
    def callback(self, channel, method, properties, body) -> None:
        pass


class Sender:
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


class Receiver:
    def __init__(self, rabbit_host: str, rabbit_port: int, channel_name: str):
        self.rabbit_host = rabbit_host
        self.rabbit_port = rabbit_port
        self.channel_name = channel_name
        self.message = None
        self.message_event = threading.Event()

    def callback(self, channel, method, properties, body) -> None:
        if not self.message_event.is_set():
            channel_name = method.routing_key
            print('Reader.callback(): Started on channel [' + channel_name + ']')
            message = str(body.decode())
            channel.basic_ack(delivery_tag=method.delivery_tag)
            if message is not None:
                print('Reader.callback(): Valid message found on channel [' + channel_name + ']')
                self.message = message
                self.message_event.set()
            print('Reader.callback(): Ended on channel [' + channel_name + ']')

    def receive(self, timeout_in_seconds: float = 5.0) -> str:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbit_host, port=self.rabbit_port))
        channel = connection.channel()
        channel.queue_declare(queue=self.channel_name)
        channel.basic_consume(queue=self.channel_name, auto_ack=False, on_message_callback=self.callback)
        connection.process_data_events()
        self.message_event.wait(timeout_in_seconds)
        connection.close()
        return self.message


class UtilsRabbitmq:
    def send(self, rabbit_host: str, rabbit_port: int, channel_name: str, message: str) -> bool:
        sender = Sender(rabbit_host, rabbit_port, channel_name)
        result = sender.send(message)
        print('UtilsRabbitmq.send(): Sent to [' + channel_name + '] channel following message [' + message + ']')
        return result

    def receive(self, rabbit_host: str, rabbit_port: int, channel_name: str, timeout_in_seconds: float = 5.0) -> str:
        receiver = Receiver(rabbit_host, rabbit_port, channel_name)
        message = receiver.receive(timeout_in_seconds=timeout_in_seconds)
        if message:
            print('UtilsRabbitmq.receive(): Received from [' + channel_name + '] channel following message [' + message + ']')
        else:
            print('UtilsRabbitmq.receive(): No messages received from [' + channel_name + '] channel')
        return message

    def consume(self, rabbit_host: str, rabbit_port: int, channel_name: str, callback: Callback) -> bool:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=rabbit_port))
        channel = connection.channel()
        channel.queue_declare(queue=channel_name)
        channel.basic_consume(queue=channel_name, auto_ack=False, on_message_callback=callback.callback)
        connection.process_data_events()
        return True
