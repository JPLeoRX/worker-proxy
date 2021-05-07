import pika

from worker_proxy_utils.utils_rabbitmq import UtilsRabbitmq, Callback

utils_rabbitmq = UtilsRabbitmq()

rabbit_host = 'localhost'
rabbit_port = 5672
channel_name = 'TESTING_CHANNEL'

class MyCallback(Callback):
    def callback(self, channel, method, properties, body) -> None:
        channel_name = method.routing_key
        print('MyCallback.callback(): Started on channel [' + channel_name + ']')
        message = str(body.decode())
        channel.basic_ack(delivery_tag=method.delivery_tag)
        if message is not None:
            print('MyCallback.callback(): Valid message found on channel [' + channel_name + ']')
            utils_rabbitmq.receive(rabbit_host, rabbit_port, message, timeout_in_seconds=1)
        print('MyCallback.callback(): Ended on channel [' + channel_name + ']')

utils_rabbitmq.send(rabbit_host, rabbit_port, 'main_channel', 'CH1')
# utils_rabbitmq.send(rabbit_host, rabbit_port, 'main_channel', 'CH2')
# utils_rabbitmq.send(rabbit_host, rabbit_port, 'CH1', 'Message 1')
# utils_rabbitmq.send(rabbit_host, rabbit_port, 'CH2', 'Message 2')

utils_rabbitmq.consume(rabbit_host, rabbit_port, 'main_channel', MyCallback())