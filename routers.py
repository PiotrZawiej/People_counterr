from fastapi import HTTPException, APIRouter
from add_task import add_task_to_queue
from receive import start_worker

router = APIRouter()

@router.get("/add_task")
async def get_photo():
    url = "https://t4.ftcdn.net/jpg/02/87/41/47/360_F_287414734_OKNLmIbSObUKIELfwEK6eu52cdRV5HAK.jpg"
    add_task_to_queue(url)

    return {"task": "added"}

router.get("/receive_task")
async def consume_task():
    start_worker()
