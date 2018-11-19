import json

#------------------------------Part1--------------------------------
# Here we define our Lambda function and configure what it does when 
# an event with a Launch, Intent and Session End Requests are sent. # The Lambda function responses to an event carrying a particular 
# Request are handled by functions such as on_launch(event) and 
# intent_scheme(event).

def lambda_handler(event, context):
        
    if event['session']['new']:
        on_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event['request']['type'] == "IntentRequest":
       return on_intent(event["request"], event["session"])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()

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
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
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
    speech_output = "There is a person at your door which I am 50% confident about"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        speech_output, should_end_session))
        
#Function to return the response for custom Intent request
def get_door_status():
    session_attributes = {}
    speech_output = "There is a new guest at your door"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        speech_output, should_end_session))
        
#Function to return the response for AMAZON.HelpIntent
def get_help_response():
    session_attributes = {}
    speech_output = "How can I help you?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        speech_output, should_end_session))

#Function to return the response for AMAZON.StopIntent or AMAZON.CancelIntent
def handle_session_end_request():
    session_attributes = {}
    speech_output = "Thank you for using the skill.  See you next time!"
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))
    
#----------------------------Part4----------------------------------  
#Here we define the functions that returns the response back to the alexa 

def build_speechlet_response(output, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "shouldEndSession": should_end_session
    }
    
def build_response(session_attributes, speechlet_response):
     return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
