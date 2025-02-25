import pika
import sys
import json



def send_message_to_queue(queue_name: str, message: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2  
        )
    )

    connection.close()
    print(f"Message sent to {queue_name}: {message}")
