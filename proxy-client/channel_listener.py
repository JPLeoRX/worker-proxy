import threading
import pika
from channel_callback import ChannelCallback
from injectable import injectable, autowired, Autowired
from worker_proxy_utils import UtilsEnv


@injectable
class ChannelListener:
    @autowired
    def __init__(self, utils_env: Autowired(UtilsEnv), channel_callback: Autowired(ChannelCallback)):
        self.utils_env = utils_env
        self.callback = channel_callback

    def register_async(self):
        thread = threading.Thread(target=self.register, args=[])
        thread.start()

    def register(self):
        rabbitmq_config = self.utils_env.get_rabbitmq_config()
        credentials = pika.PlainCredentials(rabbitmq_config.username, rabbitmq_config.password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_config.host, port=rabbitmq_config.port, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue='channels')
        channel.basic_consume(queue='channels', auto_ack=False, on_message_callback=self.callback.callback)
        channel.start_consuming()
