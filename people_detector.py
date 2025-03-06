import cv2
from PIL import Image
import requests
import numpy as np

def get_photo_from_web(url):
    response = requests.get(url, stream=True)
    
    pil_image = Image.open(response.raw)
    
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


def people_detector(image):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    (rects, weights) = hog.detectMultiScale(image, winStride=(8, 8), padding=(20, 20), scale=1.1)

    num_humans = len(rects)

    for (x, y, w, h) in rects:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite("output.jpg", image)

    return num_humans
