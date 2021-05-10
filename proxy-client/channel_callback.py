import json
import threading
from injectable import injectable, autowired, Autowired
from worker_proxy_message_protocol import ProxyChannel
from worker_proxy_utils import RabbitmqConsumerCallback
from channel_processor import ChannelProcessor


@injectable
class ChannelCallback(RabbitmqConsumerCallback):
    @autowired
    def __init__(self, channel_processor: Autowired(ChannelProcessor)):
        self.processor = channel_processor

    def callback(self, channel, method, properties, body) -> None:
        channel_name = method.routing_key
        print('ChannelCallback.callback(): Started on channel [' + channel_name + ']')
        message = str(body.decode())
        channel.basic_ack(delivery_tag=method.delivery_tag)
        if message is not None:
            print('ChannelCallback.callback(): Valid message found on channel [' + channel_name + ']')
            self.process_async(message)
        print('ChannelCallback.callback(): Ended on channel [' + channel_name + ']')

    def process_async(self, received_new_message: str):
        thread = threading.Thread(target=self.process, args=[received_new_message])
        thread.start()
        return

    def process(self, received_new_message: str):
        proxy_channel = ProxyChannel.parse_obj(json.loads(received_new_message))
        print('ChannelCallback.process(): Parsed proxy channel ' + str(proxy_channel))
        self.processor.process(proxy_channel)
