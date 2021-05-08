import os
import threading
import json
import requests

import pika
import worker_proxy_utils
from injectable import load_injection_container
load_injection_container()
load_injection_container(str(os.path.dirname(worker_proxy_utils.__file__)))
from fastapi import FastAPI
from worker_proxy_utils import RabbitmqConsumerCallback, UtilsRabbitmq
from worker_proxy_message_protocol import ProxyChannel, ProxyRequest, ProxyResponse, ProxyErrorResponse

app = FastAPI()
rabbit_host = 'localhost'
rabbit_port = 5672
channel_name = 'channels'

class ChannelProcessor():
    def __init__(self):
        self.utils_rabbitmq = UtilsRabbitmq()

    def process(self, received_proxy_channel: ProxyChannel):
        proxy_request_message = self.utils_rabbitmq.receive(rabbit_host, rabbit_port, received_proxy_channel.request_id)
        proxy_request = ProxyRequest.parse_obj(json.loads(proxy_request_message))
        print('ChannelProcessor.process(): Parsed proxy request ' + str(proxy_request))

        # Build new url
        new_base_url = 'http://localhost:7000/'
        old_url = str(proxy_request.url)
        old_base_url = str(proxy_request.base_url)
        old_path_url = old_url.replace(old_base_url, '')
        new_url = new_base_url + old_path_url

        # Make request
        try:
            forwarded_response = None
            if proxy_request.method == 'GET':
                forwarded_response = requests.get(new_url, headers=proxy_request.headers)
            elif proxy_request.method == 'POST':
                forwarded_response = requests.post(new_url, data=proxy_request.body, headers=proxy_request.headers)
            elif proxy_request.method == 'PUT':
                forwarded_response = requests.put(new_url, data=proxy_request.body, headers=proxy_request.headers)
            elif proxy_request.method == 'DELETE':
                forwarded_response = requests.delete(new_url, headers=proxy_request.headers)
            else:
                raise RuntimeError("Unsupported method: " + proxy_request.method)
            print('ChannelProcessor.process(): Forwarded from [' + old_url + '] to [' + new_url + ']')
            proxy_response = ProxyResponse(forwarded_response.content, forwarded_response.status_code, forwarded_response.headers)
            self.utils_rabbitmq.send(rabbit_host, rabbit_port, received_proxy_channel.response_id, str(proxy_response.json()))
            return
        except requests.exceptions.ConnectionError:
            proxy_error_response = ProxyErrorResponse(received_proxy_channel.id, 'NO_CONNECTION_TO_WORKER', 'The worker\'s proxy client has received and tried to process request, but failed to establish connection to proxied service url [' + new_url + ']')
            print('ChannelProcessor.process(): Failed to forward from [' + old_url + '] to [' + new_url + ']')
            proxy_response = ProxyResponse(str(proxy_error_response.json()), 500, {"Content-Type": "application/json"})
            self.utils_rabbitmq.send(rabbit_host, rabbit_port, received_proxy_channel.response_channel, str(proxy_response.json()))
            return


class ChannelCallback(RabbitmqConsumerCallback):
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
        processor = ChannelProcessor()
        processor.process(proxy_channel)
        #message = utils_rabbitmq.receive(rabbit_host, rabbit_port, received_new_channel, timeout_in_seconds=1)
        #print('Processed ' + message)

class ChannelListener():
    def register_async(self):
        self.thread = threading.Thread(target=self.register, args=[])
        self.thread.start()

    def register(self):
        callback = ChannelCallback()
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=rabbit_port))
        channel = connection.channel()
        channel.queue_declare(queue=channel_name)
        channel.basic_consume(queue=channel_name, auto_ack=False, on_message_callback=callback.callback)
        channel.start_consuming()

listener = ChannelListener()
listener.register()
