import pika
import sys
from datetime import datetime
from uuid import uuid4

eventid = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())

def get_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    

    return connection


def declare_queue(channel):
    channel.queue_declare(queue='people_detector')

connection = get_connection()
channel = connection.channel()

declare_queue(channel)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='people_detector',
                      body='Hello World!...')

print(f" [x] Sent", message)

connection.close()