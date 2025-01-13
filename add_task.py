import pika
import sys
import json



def get_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    

    return connection


def declare_queue(channel):
    channel.queue_declare(queue='people_detector', durable=True)



def add_task_to_queue(url : str, eventID):

    connection = get_connection()
    channel = connection.channel()

    declare_queue(channel)

    message = json.dumps({"url": url, "eventID": eventID})
    
    print(f"Sending message: {message}")
    channel.basic_publish(exchange='',
                        routing_key='people_detector',
                        body= message,
                        properties=pika.BasicProperties(
                            delivery_mode = pika.DeliveryMode.Persistent
                        ))

    connection.close()
    return {"message": "Task added to queue", "eventid": eventID}

