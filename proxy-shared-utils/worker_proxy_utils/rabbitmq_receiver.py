import threading
import pika


class RabbitmqReceiver:
    def __init__(self, rabbit_host: str, rabbit_port: int, channel_name: str, debug: bool = False):
        self.rabbit_host = rabbit_host
        self.rabbit_port = rabbit_port
        self.channel_name = channel_name
        self.message = None
        self.message_event = threading.Event()
        self.debug = debug

    def callback(self, channel, method, properties, body) -> None:
        # If the event is still not completed
        if not self.message_event.is_set():
            channel_name = method.routing_key
            if self.debug:
                print('RabbitmqReceiver.callback(): Started on channel [' + channel_name + ']')
            message = str(body.decode())
            channel.basic_ack(delivery_tag=method.delivery_tag)

            # If valid message was found - save it and emit the event
            if message is not None:
                if self.debug:
                    print('RabbitmqReceiver.callback(): Valid message found on channel [' + channel_name + ']')
                self.message = message
                self.message_event.set()

            if self.debug:
                print('RabbitmqReceiver.callback(): Ended on channel [' + channel_name + ']')

    def receive(self, timeout_in_seconds: float = 5.0) -> str:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbit_host, port=self.rabbit_port))
        channel = connection.channel()
        channel.queue_declare(queue=self.channel_name)
        channel.basic_consume(queue=self.channel_name, auto_ack=False, on_message_callback=self.callback)
        connection.process_data_events()
        self.message_event.wait(timeout_in_seconds)
        connection.close()
        return self.message
