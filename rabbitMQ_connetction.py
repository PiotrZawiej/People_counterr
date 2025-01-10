import pika

def get_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    

    return connection


def declare_queue(channel):
    channel.queue_declare(queue='people_detector')

connection = get_connection()
channel = connection.channel()

declare_queue(channel)

channel.basic_publish(exchange='',
                      routing_key='people_detector',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

connection.close()