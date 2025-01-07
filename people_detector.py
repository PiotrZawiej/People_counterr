import cv2

def people_detector(photo_dir):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    image = cv2.imread(photo_dir)

    (rects, weights) = hog.detectMultiScale(image, winStride=(7, 7), padding=(8, 8), scale=1.05)

    num_humans = len(rects)

    for (x, y, w, h) in rects:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite("output.jpg", image)

    return num_humans
