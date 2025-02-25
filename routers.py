from fastapi import HTTPException, APIRouter, UploadFile, File
from add_task import send_message_to_queue
from uuid import uuid4
from datetime import datetime
from io import BytesIO
from PIL import Image
from people_detector import people_detector
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
        method_frame, header_frame, body = channel.basic_get(queue='results_queue', auto_ack=True)
        if not body:
            break  
        
        result = json.loads(body)
        if result.get("eventID") == eventid:
            return {"eventID": eventid, "result": result}  

    return {"eventID": eventid, "status": "Task not yet processed"}


# @router.post("/upload_image")
# async def upload_image(file: UploadFile = File(...)):
#     eventid = generate_eventid()

#     try:
#         file_content = await file.read()
#         image = Image.open(BytesIO(file_content))

#         people_count = people_detector(image)

#         result_store[eventid] = {"status": "completed", "human_count": people_count}

#         return {"eventid": eventid, "status": "completed", "human_count": people_count}

#     except Exception as e:
#         result_store[eventid] = {"status": "failed", "error": str(e)}
#         raise HTTPException(status_code=400, detail=f"Error processing the image: {str(e)}")


