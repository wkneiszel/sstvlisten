import os
import subprocess
from datetime import datetime
import requests
from dtmfstream import detect_tone
import pyttsx3
from picamera import PiCamera
from time import sleep
import urllib.request

BASE_DIR = os.getcwd()
ROBOT36_DIR = os.path.join(BASE_DIR, 'robot36')
SERVER_URL = 'http://192.168.0.235:8000/api/images/'
USERNAME = 'station'
PASSWORD = 'RaspberryPi'
CALLSIGN = "W9WJK"

camera = PiCamera()

def sstv_decode():
    os.chdir(ROBOT36_DIR)
    subprocess.call(['./decode', 'plughw:CARD=Device', 'newimage.ppm'])
    current_time = datetime.now()
    filename = current_time.strftime("%Y%m%d%H%M%S") + '.png'
    subprocess.call(['ffmpeg', '-i', 'newimage.ppm', filename])
    upload_image = open(filename, 'rb')
    data = {'photo':upload_image}
    post_request = requests.post(SERVER_URL, files=data, auth=(USERNAME, PASSWORD))
    os.remove(filename)

def speak(words):
    engine = pyttsx3.init()
    #engine.setProperty('voice', 'english-us')
    #engine.setProperty('rate', 150)
    engine.say(words)
    engine.runAndWait()

def identify():
    speak(CALLSIGN)
    
def encode(filename):
    os.chdir(ROBOT36_DIR)
    subprocess.call(['./encode', filename])
    os.remove(filename)
    
def create_ppm(filename):
    current_time = datetime.now()
    output_filename = current_time.strftime("%Y%m%d%H%M%S") + '.ppm'
    subprocess.call(['ffmpeg', '-i', filename, '-vf', 'scale=320:240', output_filename])
    return(output_filename)

def take_new_photo():
    os.chdir(ROBOT36_DIR)
    filename = os.path.join(ROBOT36_DIR, 'capture.jpg')
    camera.capture(filename)
    return(create_ppm(filename))

def get_most_recent():
    os.chdir(ROBOT36_DIR)
    endpoint = SERVER_URL + "most_recent/"
    image_info = requests.get(endpoint).json()
    fileurl = image_info['photo']
    filename = "mostrecent.png"
    urllib.request.urlretrieve(fileurl, filename)
    return(create_ppm(filename))

def get_random():
    os.chdir(ROBOT36_DIR)
    endpoint = SERVER_URL + "random/"
    image_info = requests.get(endpoint).json()
    fileurl = image_info['photo']
    filename = "random.png"
    urllib.request.urlretrieve(fileurl, filename)
    return(create_ppm(filename))

if __name__ == '__main__':
    while True:
        action = detect_tone()
        if(action == '1'):
            speak("w9wjk listening for SSTV robot36 mode")
            sstv_decode()
            speak("image received")
            identify()
        if(action == '2'):
            speak("w9wjk transmitting current view SSTV robot36 mode")
            encode(take_new_photo())
            identify()
        if(action == '3'):
            speak("w9wjk transmitting most recent image from database SSTV robot36 mode")
            encode(get_most_recent())
            identify()
        if(action == '4'):
            speak("w9wjk transmitting random image from database SSTV robot36 mode")
            encode(get_random())
            identify()