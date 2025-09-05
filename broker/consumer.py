import os

import pika

from bloggy.environment import ENV

url = os.environ.get("CLOUDAMQP_URL", ENV.str("LOCALHOSTAMQP_URL"))
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()  # start a channel
channel.exchange_declare(exchange="test_exchange", exchange_type="direct")
channel.queue_declare(queue="test_queue")
channel.queue_bind(exchange="test_exchange", queue="test_queue", routing_key="test")


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume("test_queue", callback, auto_ack=True)
print(" [*] Waiting for messages. To exit press CTRL+C")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
