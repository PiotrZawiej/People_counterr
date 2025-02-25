import pika, time, json
from people_detector import get_photo_from_web, people_detector
from add_task import send_message_to_queue


def process_task(ch, method, properties, body):    
    task = json.loads(body)

    url = task.get("url")
    eventID = task.get("eventID")  

    print(f"Processing image ID: {eventID}")

    try:
        image = get_photo_from_web(url)
        people_count = people_detector(image)

        result = {"eventID": eventID, "status": "completed", "human_count": people_count}
        print(f"People count: {people_count}")

    except Exception as e:
        print(f"Error processing task: {e}")
        result = {"eventID": eventID, "status": "failed", "error": str(e)}

    send_message_to_queue("results_queue", result)

    ch.basic_ack(delivery_tag=method.delivery_tag)

    


def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='people_detector', durable=True)

    channel.basic_consume(queue='people_detector', on_message_callback=process_task)

    print("Worker started. Waiting for tasks...")
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()
    