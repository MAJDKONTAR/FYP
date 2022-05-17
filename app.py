import time
import cv2
import numpy as np
from flask import Flask, render_template, Response, request, jsonify
from flask_socketio import SocketIO
from find_face_mesh import FaceMeshDetector

app = Flask(__name__)
socket = SocketIO(app, cors_allowed_origins="*")

output = 10
start_time = time.time()
is_motion = False
ret, jpeg = cv2.imencode('.jpg', np.ones((480, 640, 3)))
rover_frame = frame = jpeg.tobytes()
detector = FaceMeshDetector()
response = {'action': 0, 'direction': 0}
vitals = ({'time': '',
           'temperature': '--',
           'heartbeat': '--',
           'message': ''})
history = {'time': [],
           'temperature': [],
           'heartbeat': [],
           'message': []}


@app.route('/')
def home():
    return render_template('home.html', heartbeat=vitals['heartbeat'], temperature=vitals['temperature'])


@app.route('/vitals', methods=['POST', 'GET'])
def process_vitals():
    global vitals
    if request.method == 'POST':
        vitals = request.json
        history['time'].append(vitals['time'])
        history['temperature'].append(vitals['temperature'])
        history['heartbeat'].append(vitals['heartbeat'])
        history['message'].append(vitals['message'])
        print(history)
    return vitals

@app.route('/history', methods=['GET'])
def get_history():
    return history

# @app.route('/pc_feed')
# def pc_feed():
#     return Response(gen_pc_feed(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')


# def gen_pc_feed():
#     while True:
#         try:
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#         except:
#             pass


# @app.route('/rover_feed')
# def rover_feed():
#     return Response(gen_rover_feed(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')
#
#
# def gen_rover_feed():
#     while True:
#         try:
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + rover_frame + b'\r\n\r\n')
#         except:
#             pass
#
#
# @app.route('/process', methods=['POST'])
# def feed():
#     global output, is_motion, start_time, response
#     global frame
#     data = request.data
#     image = np.fromstring(data, np.uint8)
#     # print(image.shape)
#     image = image.reshape((480, 640, 3))
#     ret, jpeg = cv2.imencode('.jpg', image)
#     frame = jpeg.tobytes()
#     # ret, image = cap.read()
#     end_time = time.time()
#     detector.find_face_mesh(image, draw=False)
#     blink = detector.blink_detector(image)
#     if end_time - start_time >= 1:
#         print('Timer reset')
#         start_time = time.time()
#         detector.reset_blink()
#     if blink >= 2 and end_time - start_time < 1:
#         if is_motion:
#             print('Motion Stopped')
#             is_motion = False
#         else:
#             print('Motion Started')
#             is_motion = True
#         detector.reset_blink()
#         start_time = time.time()
#     if is_motion:
#         _, response = detector.get_head_position(5)
#     else:
#         response = {'action': 0, 'direction': 0}
#     return response


@app.route('/control', methods=['GET'])
def control():
    return response


if __name__ == '__main__':
    app.run()
