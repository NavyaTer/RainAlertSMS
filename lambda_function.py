import json
import boto3
from botocore.vendored import requests

def kelvinToFahrenheit(kelvin):
    return kelvin * 1.8 - 459.67

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
    x = requests.get('...')
    weather = x.json()

    if (weather['current']['weather'][0]['id'] == get_previous_number()):
        return "dont_notify"
    else:
        update_current_number(weather['current']['weather'][0]['id'])

    current_weather = weather['current']['weather']
    current_temp = round(kelvinToFahrenheit(weather['current']['feels_like']))
    weather_mains = []
    weather_details = []
    for weather in current_weather:
        id = weather['id']
        if False == bad_weather(id):
            continue
        weather_mains.append(weather['main'])
        weather_details.append(weather['description'])
    if not weather_mains:
        return "dont_notify"
    sentence_one = "Weather conditions are: "
    weather_mains_conditions = ' '.join(weather_mains)
    sentence_two = "You can expect: "
    weather_details_conditions = ' '.join(weather_details)
    temperature_sentence = "Current temperature is " + str(current_temp) + " degrees Fahrenheit. "
    return temperature_sentence + " " +sentence_one + weather_mains_conditions + '. ' + sentence_two + weather_details_conditions + '. - Navya'

def update_current_number(number):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("...")
    table.put_item(Item= {'prev': 'weather_code', 'prev_number' : number})

    
def get_previous_number():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table()
    data = table.get_item(Key={'prev': 'weather_code'})    
    return data['Item']['prev_number']

def lambda_handler(event, context):
    notification = weatherCall()
    if notification != "dont_notify":
        client = boto3.client('sns')
        response = client.publish (
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
