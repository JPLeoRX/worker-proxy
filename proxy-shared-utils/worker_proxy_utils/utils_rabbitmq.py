from worker_proxy_utils.rabbitmq_sender import RabbitmqSender
from worker_proxy_utils.rabbitmq_receiver import RabbitmqReceiver
from worker_proxy_utils.rabbitmq_consumer import RabbitmqConsumer
from worker_proxy_utils.rabbitmq_consumer_callback import RabbitmqConsumerCallback
from injectable import injectable


@injectable
class UtilsRabbitmq:
    def send(self, rabbit_host: str, rabbit_port: int, channel_name: str, message: str) -> bool:
        sender = RabbitmqSender(rabbit_host, rabbit_port, channel_name)
        result = sender.send(message)
        print('UtilsRabbitmq.send(): Sent to [' + channel_name + '] channel following message [' + message + ']')
        return result

    def receive(self, rabbit_host: str, rabbit_port: int, channel_name: str, timeout_in_seconds: float = 5.0) -> str:
        receiver = RabbitmqReceiver(rabbit_host, rabbit_port, channel_name)
        message = receiver.receive(timeout_in_seconds=timeout_in_seconds)
        if message:
            print('UtilsRabbitmq.receive(): Received from [' + channel_name + '] channel following message [' + message + ']')
        else:
            print('UtilsRabbitmq.receive(): No messages received from [' + channel_name + '] channel')
        return message

    def consume(self, rabbit_host: str, rabbit_port: int, channel_name: str, callback: RabbitmqConsumerCallback) -> bool:
        consumer = RabbitmqConsumer(rabbit_host, rabbit_port, channel_name)
        result = consumer.consume(callback)
        print('UtilsRabbitmq.consume(): Registered consumer on [' + channel_name + '] channel')
        return result
