import pika, json, base64
from people_detector import get_photo_from_web, people_detector
from add_task import send_message_to_queue
from PIL import Image
from io import BytesIO
import cv2
import numpy as np


def process_task(ch, method, properties, body):    
    task = json.loads(body)

    url = task.get("url")
    eventID = task.get("eventID")
    image_data = task.get("image")  

    print(f"Processing image ID: {eventID}")

    try:

        if url:
            image = get_photo_from_web(url)
        elif image_data:

            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            image = image.convert("RGB")

            image_np = np.array(image, dtype=np.uint8) 
            image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)   
        else:
            raise ValueError("No image data or URL provided")
        
        people_count = people_detector(image)

        result = {"eventID": eventID, "status": "completed", "human_count": people_count}
        print(f"People count: {people_count}")

        print(result)

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
    