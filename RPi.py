from gpiozero import *
from time import sleep
from signal import pause
from picamera import PiCamera
import time
from datetime import datetime
import requests


ledblue = LED(26)
pir = MotionSensor(19)
alarm = Buzzer(2)

camera = PiCamera()
camera.rotation = 180
camera.resolution = (1280, 720)
camera.framerate = 60
i = 0
j = 0
ledblue.off()

def capture_video():
    global i
    i = i + 1
    camera.start_recording("/home/pi/Desktop/Recordings/" + datetime.now().strftime('%A-%y-%m-%d_%H:%M:%S.h264'))

def capture_picture():
    
    
    for i in range(5):
        
        camera.capture("/home/pi/Desktop/CamPictures/" + datetime.now().strftime('%A-%y-%m-%d_%H:%M:%S:%MS.jpg'))
        sleep(.5)
    
def send_alert():
    payload = {
        'content': "Intruder Detected"
    }
    
    header = {
        'authorization': 'Key goes here' 
    }
    
    r = requests.post("Message link goes here", data=payload, headers=header)

while True:
    if pir.motion_detected:
        pir.wait_for_motion()
        capture_video()
        ledblue.on()
        capture_picture()
        send_alert()
        sleep(.5)
        pir.wait_for_no_motion()
        ledblue.off()
        sleep(.5)
        camera.stop_recording()