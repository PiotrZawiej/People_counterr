from fastapiApp import FastAPI
from people_detector import people_detector

app = FastAPI()


@app.get("/")
def get_photo():
    people_count = people_detector("picture\humans.jpg")
    return {"human_count": people_count}