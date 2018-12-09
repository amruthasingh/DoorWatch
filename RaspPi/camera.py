from picamera import PiCamera
from time import sleep
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time
import boto3
#from boto.s3.key import Key


def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("Preparing to take picture ...")
    
    camera.resolution = (240, 400)
    camera.capture('/home/pi/Desktop/image123.jpg')
    
    print("Picture captured.")
    print("--------------- \n")
    print "rekognising with AWS Reko"
    
    isHuman = imageRecko(imageFile)
    
    print str(isHuman)
    
    if isHuman:
       uploadImageToS3(imageFile)
       pubImageUploadedToIoT()
    else:
       print "No human detected. Try Again"
    
    print "--- Done ----"
    
def imageRecko(imageFile):
    isHuman = False
    with open(imageFile, 'rb') as image:
        response = reko_client.detect_labels(Image={'Bytes': image.read()})
    
    print('Detected labels in ' + imageFile)    
    for label in response['Labels']:
        if (label['Name'] == 'Human' and str(label['Confidence']) > 90):
          print (label['Name'] + ' : ' + str(label['Confidence']))
          print ("We have a visitor")
          isHuman = True
          break
        else:
          isHuman = False
          
    return isHuman

def uploadImageToS3(imageFile):
    s3_client.upload_file(imageFile, bucket, keyName, ExtraArgs={'ACL':'public-read'})    
    print "Image succesfully uploaded to s3"

def pubImageUploadedToIoT():
    url = '{}/{}/{}'.format(s3_client.meta.endpoint_url, bucket, keyName)	
    print(url)

    myPublishTopic = "imageLinkSend"
    myPublicMesaage = {}
    myPublicMesaage['text'] = "The image link is below"
    myPublicMesaage['link'] = url
    myPubMessageJson = json.dumps(myPublicMesaage)
    myMQTTClient.publish(myPublishTopic,myPubMessageJson,0)
    print "Link sent to IOT hub"
        
clientId = "myClientID1"
thingEndpoint = '****************'
certificatePath = '***************'
privateKeyPath = '*************'
rooCACertPath = '*****************'

imageFile='/home/pi/Desktop/image123.jpg'  #recko
#filename = '/home/pi/Desktop/image123.jpg'

bucket = "doorwatch-bucket"
keyName = "visitor_image.jpg"

session = boto3.Session(aws_access_key_id='*******************', aws_secret_access_key='*********************', region_name='***********')

reko_client = session.client('rekognition')
s3_client = session.client('s3')

camera = PiCamera()

#camera.start_preview()
#sleep(5)
#camera.capture('/home/pi/Desktop/image123.jpg')
#camera.stop_preview()

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

myTopic = "sendButtonClick"

myMQTTClient.subscribe(myTopic, 0, customCallback)

while True:
  None




