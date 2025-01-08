from fastapi import FastAPI
from people_detector import people_detector, get_photo_from_web

app = FastAPI()


@app.get("/")
def get_photo():
    
    return {"human_count": "people_count"}