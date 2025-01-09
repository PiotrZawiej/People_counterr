from fastapi import HTTPException, APIRouter
from people_detector import people_detector, get_photo_from_web

router = APIRouter()

@router.get("/")
def get_photo():
    url = "https://t4.ftcdn.net/jpg/02/87/41/47/360_F_287414734_OKNLmIbSObUKIELfwEK6eu52cdRV5HAK.jpg"
    image = get_photo_from_web(url)

    people_count = people_detector(image)
    return {"human_count": people_count}
