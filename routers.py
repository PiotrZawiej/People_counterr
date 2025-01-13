from fastapi import HTTPException, APIRouter
from add_task import add_task_to_queue
router = APIRouter()
from uuid import uuid4
from datetime import datetime



def generate_eventid():
    return datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())

@router.get("/add_task")
async def get_photo():
    url = "https://t4.ftcdn.net/jpg/02/87/41/47/360_F_287414734_OKNLmIbSObUKIELfwEK6eu52cdRV5HAK.jpg"
    id = generate_eventid()

    add_task_to_queue(url, id)

    return {"task": "added"}


