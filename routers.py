from fastapi import HTTPException, APIRouter, UploadFile, File
from add_task import send_message_to_queue
from uuid import uuid4
from datetime import datetime
import base64
from PIL import Image
import json
import pika


router = APIRouter()

def generate_eventid():
    return datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())

@router.get("/add_task")
async def get_photo():
    url = "https://t4.ftcdn.net/jpg/02/87/41/47/360_F_287414734_OKNLmIbSObUKIELfwEK6eu52cdRV5HAK.jpg"
    id = generate_eventid()

    task = {"eventID": id, "url": url}

    send_message_to_queue("people_detector", task)

    return {"id": id}


@router.get("/get_result")
async def get_result(eventid: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='results_queue', durable=True)

    while True:
        method_frame, header_frame, body = channel.basic_get(queue='results_queue', auto_ack=False)

        if body is None:
            return {"eventID": eventid, "status": "Task not yet processed"}  

        try:
            result = json.loads(body)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON in message"}

        if result.get("eventID") == eventid:
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)  
            return {"eventID": eventid, "result": result}


@router.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    eventid = generate_eventid()

    file_content = await file.read()
    encoded_image = base64.b64encode(file_content).decode("utf-8")  

    task = {
        "eventID": eventid,
        "url": "",  
        "image": encoded_image
    }

    send_message_to_queue("people_detector", task)

    return {"eventid": eventid, "status": "processing"}