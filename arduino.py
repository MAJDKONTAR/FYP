import random
import time
from datetime import datetime

import requests

start_time = time.time()
messages = ['Want Bathroom', 'Want to talk', 'I am Hungry', 'I am Thirsty']


def get_vitals():
    global start_time
    i = 37
    j = 80
    message = ''
    if time.time() - start_time > 5:
        i = 36
        j = 85
        message = messages[random.randint(0, 3)]
        start_time = time.time()
    t = datetime.now()
    # print(t)
    return ({'time': str(t),
             'temperature': i,
             'heartbeat': j,
             'message': message})


while True:
    time.sleep(3)
    vitals = get_vitals()
    try:
        response = requests.post('http://127.0.0.1:5000/vitals', json=vitals)
    except:
        print('ERROR')
        continue
