import time
import boto3
import requests
import json
from dotenv import load_dotenv
import os


load_dotenv()

# Load AWS SQS and keys
sqs = boto3.client('sqs', region_name='us-east-1')
queue_url = os.getenv('SQS_QUEUE_URL')
api_key = os.getenv('WEATHER_API_KEY')

# Load list of cities for debugging this part
with open('cities.txt', 'r') as file:
    cities = [line.strip() for line in file.readlines()]

def get_weather_data(city):
    '''
    fetch wether data (as JSON) for specific city
    :param city: current city which data we want to fetch
    :return: json (of the response)
    '''

    base_url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch weather data for {city}")
        return None

# Function to send message to SQS
def send_message_to_sqs(message_body):
    '''
    function for sending message to SQS
    :param message_body: the message we want to send
    :return: None
    '''
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message_body)
    )
    print(f"Message sent to SQS with ID: {response['MessageId']}")

# infinite loop to fetch weather data and send to SQS
print (cities)
while True:
    for city in cities:
        weather_data = get_weather_data(city)
        if weather_data:
            send_message_to_sqs(weather_data)
            print(f"Weather data for {city} sent to SQS")
        time.sleep(60)
