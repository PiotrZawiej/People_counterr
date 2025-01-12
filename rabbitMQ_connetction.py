import pika
import sys
from datetime import datetime
from uuid import uuid4
import json

eventid = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())

def get_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    

    return connection


def declare_queue(channel):
    channel.queue_declare(queue='people_detector', durable=True)

def add_task_to_queue(url : str):
    connection = get_connection()
    channel = connection.channel()

    declare_queue(channel)

    message = json.dumps({"url": url})
    channel.basic_publish(exchange='',
                        routing_key='people_detector',
                        body= message,
                        properties=pika.BasicProperties(
                            delivery_mode = pika.DeliveryMode.Persistent
                        ))

    connection.close()
    return {"message": "Task added to queue"}

url = "https://t4.ftcdn.net/jpg/02/87/41/47/360_F_287414734_OKNLmIbSObUKIELfwEK6eu52cdRV5HAK.jpg"
add_task_to_queue(url)
