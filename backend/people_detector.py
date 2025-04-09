import cv2
from PIL import Image
import requests
import numpy as np
import torch
import os

device = "cuda" if torch.cuda.is_available() else "cpu"
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)


def get_photo_from_web(url):
    response = requests.get(url, stream=True)
    
    pil_image = Image.open(response.raw)
    
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


def people_detector(image, image_id):
    if isinstance(image, np.ndarray):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = model(image)

    detections = results.pandas().xyxy[0]  

    people = detections[detections['name'] == 'person']

    for _, row in people.iterrows():
        x1, y1, x2, y2, conf = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax']), row['confidence']
        if conf > 0.5: 
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    output_path = os.path.join("results", f"output_{image_id}.jpg")
    cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

    return len(people)  
