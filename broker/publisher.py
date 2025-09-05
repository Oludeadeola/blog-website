import os
import pika
from bloggy.environment import ENV

"""
This script is responsible for creating a connection to the RabbitMQ server and declaring a queue named hello.
Step 1: Access the CLOUDAMQP_URL environment variable and parse it (fallback to localhost).
Step 2: Create a connection to the RabbitMQ server.
Step 3: Create a channel.
Step 4: Declare an exchange
Step 5: Declare a queue
Step 6: 
"""

# TODO: Access the CLOUDAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get("CLOUDAMQP_URL", ENV.str("LOCALHOSTAMQP_URL"))
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)

channel = connection.channel()  # start a channel
channel.exchange_declare(
    exchange="test_exchange", exchange_type="direct"
)  # Declare an exchange
channel.queue_declare(queue="test_queue")  # Declare a queue

channel.queue_bind(exchange="test_exchange", queue="test_queue", routing_key="test")

channel.basic_publish(
    body="Hello World!".encode("utf-8"), exchange="test_exchange", routing_key="hello"
)
print("Message Sent!")

channel.close()
connection.close()
