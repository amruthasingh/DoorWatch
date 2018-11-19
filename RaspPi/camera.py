import RPi.GPIO as GPIO
import time
<strong>from picamera import PiCamera</strong>
 
GPIO.setmode(GPIO.BCM)
 
pirPin = 7
GPIO.setup(pirPin, GPIO.IN, <strong>GPIO.PUD_UP</strong>)
camera = PiCamera()
counter = 1
 
while True:
    if GPIO.input(pirPin) == GPIO.LOW:
        <strong>try: </strong>
<strong>                      camera.start_preview()</strong>
<strong>                      time.sleep(1)</strong>
<strong>                      camera.capture('/home/pi/image%s.jpg' % counter)</strong>
<strong>                      counter = counter + 1</strong>
<strong>                      camera.stop_preview()
                  except:</strong>
<strong>                      camera.stop_preview()</strong>
    time.sleep(<strong>3</strong>)
