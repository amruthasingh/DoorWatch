from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time
import boto3

def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    response = polly_client.synthesize_speech(VoiceId='Joanna',
                OutputFormat='mp3', 
                Text = 'We have a visitor.')

    file = open('speech.mp3', 'w')
    file.write(response['AudioStream'].read())
    file.close()
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

clientId = "myClientID1"
thingEndpoint = '*********************'
certificatePath = '********************'
privateKeyPath = '********************'
rooCACertPath = '*******************'
polly_client = boto3.Session(
                aws_access_key_id=************,
    aws_secret_access_key=***********,
    region_name='us-west-2').client('polly')

print "before setup1 ..."

myMQTTClient = AWSIoTMQTTClient(clientId)
myMQTTClient.configureEndpoint(thingEndpoint, 8883)
myMQTTClient.configureCredentials(rooCACertPath, privateKeyPath, certificatePath)

myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myMQTTClient.connect()

print "connected"

myTopic = "imageLinkSend"

myMQTTClient.subscribe(myTopic, 0, customCallback)

while True:
  None

# i = 0
# while True:
  # i = i +1
  # message = {}
  # message['message'] = "This is message"
  # message['type'] = "This is message type"
  # message['count'] = i
  # messageJson = json.dumps(message)
  # myMQTTClient.publish(myTopic, messageJson, 0)
  # time.sleep(2)