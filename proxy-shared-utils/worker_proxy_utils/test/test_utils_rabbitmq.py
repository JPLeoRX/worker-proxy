import pika

from worker_proxy_utils.utils_rabbitmq import UtilsRabbitmq

utils_rabbitmq = UtilsRabbitmq()

rabbit_host = 'localhost'
rabbit_port = 5672
channel_name = 'TESTING_CHANNEL'

# utils_rabbitmq.send(rabbit_host, rabbit_port, 'CH1', 'Message 1')
# utils_rabbitmq.send(rabbit_host, rabbit_port, 'CH1', 'Message 2')
# utils_rabbitmq.send(rabbit_host, rabbit_port, 'CH2', 'Message 3')
# utils_rabbitmq.send(rabbit_host, rabbit_port, 'CH2', 'Message 4')

utils_rabbitmq.receive(rabbit_host, rabbit_port, 'CH1')
utils_rabbitmq.receive(rabbit_host, rabbit_port, 'CH2')