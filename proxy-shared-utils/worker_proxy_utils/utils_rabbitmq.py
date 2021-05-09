from worker_proxy_message_protocol import RabbitmqConfig
from worker_proxy_utils.rabbitmq_sender import RabbitmqSender
from worker_proxy_utils.rabbitmq_receiver import RabbitmqReceiver
from injectable import injectable


@injectable
class UtilsRabbitmq:
    def send(self, rabbitmq_config: RabbitmqConfig, channel_name: str, message: str) -> bool:
        sender = RabbitmqSender(rabbitmq_config, channel_name)
        result = sender.send(message)
        print('UtilsRabbitmq.send(): Sent to [' + channel_name + '] channel following message [' + message + ']')
        return result

    def receive(self, rabbitmq_config: RabbitmqConfig, channel_name: str, timeout_in_seconds: float = 5.0) -> str:
        receiver = RabbitmqReceiver(rabbitmq_config, channel_name)
        message = receiver.receive(timeout_in_seconds=timeout_in_seconds)
        if message:
            print('UtilsRabbitmq.receive(): Received from [' + channel_name + '] channel following message [' + message + ']')
        else:
            print('UtilsRabbitmq.receive(): No messages received from [' + channel_name + '] channel')
        return message
