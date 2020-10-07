import os
import subprocess
from datetime import datetime
import requests

BASE_DIR = os.getcwd()
ROBOT36_DIR = os.path.join(BASE_DIR, 'robot36')
SERVER_URL = 'http://192.168.0.235:8000/api/images/'

os.chdir(ROBOT36_DIR)

while True:
    subprocess.call(['./decode', 'plughw:CARD=Device', 'newimage.ppm'])
    current_time = datetime.now()
    filename = current_time.strftime("%Y%m%d%H%M%S") + '.png'
    subprocess.call(['ffmpeg', '-i', 'newimage.ppm', filename])
    upload_image = open(filename, 'rb')
    data = {'photo':upload_image}
    post_request = requests.post(SERVER_URL, files=data)
    os.remove(filename)
