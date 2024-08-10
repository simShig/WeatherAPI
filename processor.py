import boto3
import json
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

# Load AWS SQS and keys
queue_url = os.getenv('SQS_QUEUE_URL')
sqs = boto3.client('sqs', region_name="us-east-1")

# SQLite DB connect, create if needed
conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_name TEXT,
    location_country TEXT,
    location_localtime TEXT,
    temp_c REAL,
    condition_text TEXT
);
''')
conn.commit()

def process_weather_data(message):
    '''
    get message from the queue, process the message and save to DB
    :param message: message recieved from queue (SQS)
    :return: None (saves data to DB)
    '''

    body = message.get('Body')
    if not body:
        print("Empty message received. Skipping.")
        return

    # print(f"Raw message body: {body}")
    try:
        data = json.loads(body)
        location_name = data['location']['name']
        location_country = data['location']['country']
        location_localtime = data['location']['localtime']
        temp_c = data['current']['temp_c']
        condition_text = data['current']['condition']['text']


        cursor.execute('''
        INSERT INTO weather (location_name, location_country, location_localtime, temp_c, condition_text)
        VALUES (?, ?, ?, ?, ?)
        ''', (location_name, location_country, location_localtime, temp_c, condition_text))

        conn.commit()
        print(f"[V] Data saved for {location_name}, {location_country} at {location_localtime}  [its now {temp_c} c*,{condition_text}].")

    except json.JSONDecodeError as e:
        print(f"[X] Failed to decode JSON: {e}, raw message was: {body}")
    except Exception as e:
        print(f"[X] An error occurred: {e}")


# infinite loop to fetch massages from SQS and process to the DB
while True:
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20
    )

    messages = response.get('Messages', [])
    for message in messages:
        process_weather_data(message)
        # delete massage from queue after processing
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )
        print("Message deleted from queue")
