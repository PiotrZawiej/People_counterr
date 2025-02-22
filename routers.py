from fastapi import HTTPException, APIRouter, UploadFile, File
from add_task import add_task_to_queue
from uuid import uuid4
from datetime import datetime
from receive import result_store
from io import BytesIO
from PIL import Image
from people_detector import people_detector


router = APIRouter()

def generate_eventid():
    return datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())

@router.get("/add_task")
async def get_photo():
    url = "https://t4.ftcdn.net/jpg/02/87/41/47/360_F_287414734_OKNLmIbSObUKIELfwEK6eu52cdRV5HAK.jpg"
    id = generate_eventid()

    add_task_to_queue(url, id)

    return {"id": id}


@router.get("/get_result")
async def get_result(eventid: str):
    if eventid in result_store:
        result = result_store[eventid]
        return {"eventid": eventid, "result": result}
    else:
        return {"eventid": eventid, "status": "Task not yet processed"}


@router.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    eventid = generate_eventid()

    try:
        file_content = await file.read()
        image = Image.open(BytesIO(file_content))

        people_count = people_detector(image)

        result_store[eventid] = {"status": "completed", "human_count": people_count}

        return {"eventid": eventid, "status": "completed", "human_count": people_count}

    except Exception as e:
        result_store[eventid] = {"status": "failed", "error": str(e)}
        raise HTTPException(status_code=400, detail=f"Error processing the image: {str(e)}")


