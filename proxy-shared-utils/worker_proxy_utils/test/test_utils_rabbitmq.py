import threading
import time

import pika

from worker_proxy_utils.rabbitmq_consumer_callback import RabbitmqConsumerCallback
from worker_proxy_utils.utils_rabbitmq import UtilsRabbitmq

utils_rabbitmq = UtilsRabbitmq()

rabbit_host = 'localhost'
rabbit_port = 5672
channel_name = 'TESTING_CHANNEL'

class MyCallback(RabbitmqConsumerCallback):
    def callback(self, channel, method, properties, body) -> None:
        channel_name = method.routing_key
        print('MyCallback.callback(): Started on channel [' + channel_name + ']')
        message = str(body.decode())
        channel.basic_ack(delivery_tag=method.delivery_tag)
        if message is not None:
            print('MyCallback.callback(): Valid message found on channel [' + channel_name + ']')
            self.process_async(message)
        print('MyCallback.callback(): Ended on channel [' + channel_name + ']')

    def process_async(self, received_new_channel: str):
        thread = threading.Thread(target=self.process, args=[received_new_channel])
        thread.start()
        return

    def process(self, received_new_channel: str):
        time.sleep(20)
        message = utils_rabbitmq.receive(rabbit_host, rabbit_port, received_new_channel, timeout_in_seconds=1)
        print('Processed ' + message)

utils_rabbitmq.send(rabbit_host, rabbit_port, 'main_channel', 'CH1')
utils_rabbitmq.send(rabbit_host, rabbit_port, 'main_channel', 'CH2')
utils_rabbitmq.send(rabbit_host, rabbit_port, 'CH1', 'Message 1')
utils_rabbitmq.send(rabbit_host, rabbit_port, 'CH2', 'Message 2')

utils_rabbitmq.consume(rabbit_host, rabbit_port, 'main_channel', MyCallback())