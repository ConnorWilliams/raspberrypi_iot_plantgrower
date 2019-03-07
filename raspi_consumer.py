# This file contains code which consumes a queue from RabbitMQ in the form of (pin_number, status) and uses GPIO.Pi to reflect that state.

import pika
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
logger = logging.getLogger(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.exchange_declare(
    exchange='plantgrower',
    exchange_type='direct'
)

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

grow_number = 1
binding_key = 'to_grow/' + str(grow_number)

channel.queue_bind(
    exchange='plantgrower',
    queue=queue_name,
    routing_key=binding_key
)

logger.info('Waiting for instructions and sensors...')


def callback(ch, method, properties, body):
    logger.info(f"Received: {body}")


channel.basic_consume(
    callback,
    queue=queue_name,
    no_ack=True
)

channel.start_consuming()
