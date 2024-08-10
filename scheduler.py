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
db_path = os.getenv('DB_NAME')


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
    if response.status_code == 400:
        print(f"Failed to fetch weather data for {city} (city unavailable)")
    else:
        print(f"Failed to fetch weather data for {city} (server\API connection issue)")
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


def main():

    # Load list of cities for debugging this part
    with open('cities.txt', 'r') as file:
        cities = [line.strip() for line in file.readlines()]

    print (cities)

# infinite loop to fetch weather data and send to SQS
    while True:
        for city in cities:
            weather_data = get_weather_data(city)
            if weather_data:
                try:
                    send_message_to_sqs(weather_data)
                    print(f"Weather data for {city} sent to SQS")
                except Exception as e:
                    print(f"An error occurred, Check SQS URL.\n{e}")
                    exit(-1)
            time.sleep(60)

if __name__ == '__main__':
    main()