import json
import boto3
import datetime
import time
import subprocess
from boto3 import dynamodb 
from boto3.dynamodb.conditions import Key, Attr

#test = boto3.client('lambda')
#------------------------------Part1--------------------------------
# Here we define our Lambda function and configure what it does when 
# an event with a Launch, Intent and Session End Requests are sent. # The Lambda function responses to an event carrying a particular 
# Request are handled by functions such as on_launch(event) and 
# intent_scheme(event).

iot_client = boto3.client('iot-data')

def lambda_handler(event, context):
    #STATE_KEY = 'state_stages'
    if event['session']['new']:
        on_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event['request']['type'] == "IntentRequest":
       return on_intent(event["request"], event["session"])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()
        
   
   # return {
    #    'statusCode': 200,
     #   'body': json.dumps('Done!')
    #}

#------------------------------Part2--------------------------------
# Here we define the Request handler functions

#Handles the new session
def on_start():
    print("Session Started.")
    
#Handles Launch request
def on_launch(launch_request, session):
   return get_welcome_response()

#Handles Intent request
def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]
    if intent_name == "CheckTheDoor":
         return get_door_status()
    if intent_name == "NoVisitor":
         return get_no_visitor_status()
    #if intent_name == "LightLED":
         #return turn_lights_on()
    #elif intent_name == "DisplayImage":
         #return display_image()
    if intent_name == "Sure":
        #iot_client = boto3.client('iot-data', region_name='us-east-1')
         response = iot_client.publish( topic= "lightLed", qos=1, payload=json.dumps({"light":"on"}))
         return turn_lights_on()
    if intent_name == "Sample":
         return known_visitor()
    elif intent_name == "AMAZON.HelpIntent":
         return get_help_response()
    elif intent_name == "AMAZON.YesIntent":
         #state =  session.attributes.get(STATE_KEY)
         #if((session_attributes = {}) == '124'):
             #return turn_lights_on()
         #else:
            
        s3 = boto3.client('s3')
    
        bucket_name = 'doorwatch-bucket'
        get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
    
        objs = s3.list_objects_v2(Bucket=bucket_name)['Contents']
        val = [obj['Key'] for obj in sorted(objs, key=get_last_modified, reverse=True)]
    
        bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucket_name)
    
        object_url = "https://s3.amazonaws.com/{0}/{1}".format(bucket_name, val[0])
        print object_url  
        string = '<img src="'+object_url+'">'
        encoded_string = string.encode("utf-8")

        bucket_name = "doorwatch-bucket"
        file_name = "index.html"
        s3_path = file_name

        s3 = boto3.resource("s3")
        s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
        return display_image()
    elif intent_name == "AMAZON.NoIntent":
         return handle_something()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
         return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

#Handles the SessionEndedRequest   
def on_end():
    print("Session Ended.")

#----------------------------Part3----------------------------------   
#Here we define the functions that returns the response based on the request initiated by 
#the user. We handle the Launch request, Custom Intent request, AMAZON.HelpIntent and AMAZON.StopIntent

#Function to return the response for launch request
def get_welcome_response():
    session_attributes = {}
    speech_output = "Hi there. What you want me to do" 
    #speech_output = """Welcome to the Alexa DoorFeed skill.
                    #Let me explain you about DoorWatch project.
                    #DoorWatch is a smart door security system, which informs the users whenever there is a visitor at the door 
                    #and displays the image on user request."""
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text, should_end_session))
        
#Function to return the response for custom Intent request
def get_door_status():
    session_attributes = {}
    speech_output = "Looks like you have a visitor"
    reprompt_text = "Do you want me to show the image of the visitor"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text, should_end_session))
        
def get_no_visitor_status():
    session_attributes = {}
    speech_output = "Did you hear any notification. Sorry, I dont see anyone at the front door. Do you want me to help you out with other things like switching On the light at the front door"
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text, should_end_session))
        
def turn_lights_on():
    session_attributes = {}
    speech_output = "There you go, lights turned on"
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text, should_end_session))
        
def known_visitor():
    dynamodb = boto3.client('dynamodb')
    #dynamodb=boto3.resource("dynamodb")
    #table=dynamodb.Table('doorwatch')
    #response=dynamodb.get_item(TableName='doorwatch', key={'Name':{'S':'Zankhna'}})
    #item = response['Item']
    #a=dynamodb.get_item(Key= {'Name'})
    #response = table.get_item(Key={'Name'})
    response=dynamodb.Query(
        TableName="doorwatch", ScanIndexForward=False, limit=1)
    #Query(hash_key=HASH_KEY, ScanIndexForward=True, limit=1)
        #Key={'Name'})
    #for i in response['Items']:
        #print('Items')
    print response
    session_attributes = {}
    speech_output = "known visitor is at your door"
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text, should_end_session))
    
#Function to invoke the other lambda for displaying the image    
def display_image():
    session_attributes = {}
    speech_output = "Displayed the image of visitor"
    reprompt_text = ""
    should_end_session = False
    #print("In display func")
    #try:
        #response = test.invoke(FuntionName='display',
                               #InvocationType = 'RequestResponse')
    #except Exception as e:
        #print(e)
        #raise(e)
    #print(response)
    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text, should_end_session))
    
#Function to return the response for AMAZON.HelpIntent
def get_help_response():
    session_attributes = {}
    speech_output = "How can I help you? You can ask me to check your door feed and display the image of visitor"
    reprompt_text = "Did you find it helpful?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text, should_end_session))

#Function to return the response for AMAZON.StopIntent or AMAZON.CancelIntent
def handle_session_end_request():
    session_attributes = {}
    speech_output = "Thank you for using the skill.  See you next time! Bye Bye. have a nice day !"
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, reprompt_text, should_end_session))
    
#----------------------------Part4----------------------------------  
#Here we define the functions that returns the response back to the alexa 

def build_speechlet_response(output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }
    
def build_response(session_attributes, speechlet_response):
     return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
    
   
