import json
import boto3
from botocore.vendored import requests

#Converts kelvin temperature to fahrenheit
def kelvinToFahrenheit(kelvin):
    return kelvin * 1.8 - 459.67

#sets condition for bad weather. if else checks to determine if the current weather is bad
def bad_weather(id):
    if ((id>= 200) and (id< 300)):
        return True
    elif ((id>= 300) and (id< 400)):
        return True
    elif ((id>= 500) and (id< 600)):
        return True
    else:
        return False

def weatherCall():
    #this is making the call to the open weather API. and the open weather API tells us what the current weather at the hour is
    #x is considered the response when we ask for the weather
    x = requests.get('...')
    #we extract the json and name it weather variable
    weather = x.json()
    #if the current weather is same as previous weather, we dont notify. Else we update our database with the number form the current weather
    if (weather['current']['weather'][0]['id'] == get_previous_number()):
        return "dont_notify"
    else:
        update_current_number(weather['current']['weather'][0]['id'])
    #grabs data from the json to create our response
    current_weather = weather['current']['weather']
    current_temp = round(kelvinToFahrenheit(weather['current']['feels_like']))
    weather_mains = []
    weather_details = []
    #if there is bad weather we notify. if there is not bad weather we return "dont_notify"
    for weather in current_weather:
        id = weather['id']
        if False == bad_weather(id):
            continue
        weather_mains.append(weather['main'])
        weather_details.append(weather['description'])
    if not weather_mains:
        return "dont_notify" #this is the response if we don't have bad weather
    sentence_one = "Weather conditions are: "
    weather_mains_conditions = ' '.join(weather_mains)
    sentence_two = "You can expect: "
    weather_details_conditions = ' '.join(weather_details)
    temperature_sentence = "Current temperature is " + str(current_temp) + " degrees Fahrenheit. "
    #here we are just returning our response that we show on the text message
    return temperature_sentence + " " +sentence_one + weather_mains_conditions + '. ' + sentence_two + weather_details_conditions + '. - Navya'

#We update the key-value pair with the new number as the value. assigns new value to the weather code and stores it in the dynamo database
def update_current_number(number):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("...")
    table.put_item(Item= {'prev': 'weather_code', 'prev_number' : number})

#We check what the previous code in the database was like. And we return the previous number
def get_previous_number():
    #connect to the previous database
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table()
    #get the actual key-value pair, similar to a python dictionary, and return the previous number
    data = table.get_item(Key={'prev': 'weather_code'})    
    return data['Item']['prev_number']

def lambda_handler(event, context):
    '''
    This makes a call to the weather API. If the weatherCall method returns "dont_notify then we dont send anything to the phones.
    Otherwise, we are going to publish a message on the SNS (simple notification service) topic. 
    '''
    notification = weatherCall()
    if notification != "dont_notify":
        #we connect to the SNS topic
        client = boto3.client('sns')
        response = client.publish (
            #this is the specific address of the topic we wants
            TargetArn = {...},
            Message = json.dumps({'default': notification}),
            MessageStructure = 'json'
        )
    else:
        response = ""
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
