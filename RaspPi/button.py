mport RPi.GPIO as GPIO
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time

clientId = "myClientID"
thingEndpoint = '**************************'
certificatePath = '***************************'
privateKeyPath = '*********************'
rooCACertPath = '******************'
print "before setup1 ..."

myMQTTClient = AWSIoTMQTTClient(clientId)
myMQTTClient.configureEndpoint(thingEndpoint, 8883)
myMQTTClient.configureCredentials(rooCACertPath, privateKeyPath, certificatePath)

myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish q  myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
print "before connection..."

myMQTTClient.connect()

print "connected"

myTopic = "sendButtonClick"
message = {}
message['text'] = "This is message"
message['type'] = "This is message type"
messageJson = json.dumps(message)


def ButtonClick():
  print 'I am clicked...'
  myMQTTClient.publish(myTopic, messageJson, 0)
  
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#Button to GPIO10

while True:
 click = GPIO.input(10)
 if click == GPIO.HIGH:
  ButtonClick()
  time.sleep(0.5)

GPIO.cleanup()


