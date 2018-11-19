import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
pirPin = 7
GPIO.setup(pirPin, GPIO.IN, <strong>GPIO.PUD_UP</strong>)
 
while True:
    if GPIO.input(pirPin) == GPIO.LOW:
        print "Motion detected!"
    else:
        print "No motion"
    time.sleep(0.2)
