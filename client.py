import time
import cv2
import requests

cap = cv2.VideoCapture(0)
while True:
    try:
        start_time = time.time()
        ret, frame = cap.read()
        response = requests.post('http://127.0.0.1:5000/process', data=bytes(frame))
        response = response.json()
        print(response)
        print("FPS: ", 1.0 / (time.time() - start_time))
    except:
        continue