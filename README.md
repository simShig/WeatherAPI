# **Weather Data Processor and API**

## **Project Overview**

This project is a Python-based system that fetches weather data for a list of cities, processes the data, and exposes it via a RESTful API. It utilizes the WeatherAPI for data retrieval, AWS SQS for message queuing, and SQLite for local data storage. The system is composed of three main components:

- **Scheduler**: Fetches weather data for specified cities and pushes the data to an SQS queue.
- **Processor**: Retrieves messages from the SQS queue, processes the weather data, and stores it in a SQLite database.
- **API**: Exposes the stored weather data through a RESTful endpoint.

## **Features**

- **Weather Data Fetching**: Periodically fetches real-time weather data for a list of cities using the WeatherAPI.
- **Message Queuing**: Utilizes AWS SQS to queue weather data for processing.
- **Data Storage**: Processes and stores weather data in a SQLite database.
- **REST API**: Provides a RESTful API to access the stored weather data by country.

## **Architecture**

The project is structured into three main components:

1. **Scheduler**: A console application that:
   - Runs indefinitely.
   - Fetches weather data every minute for a list of cities.
   - Pushes the fetched data to an AWS SQS queue.

2. **Processor**: A console application that:
   - Polls the SQS queue for messages.
   - Processes each message by extracting weather data.
   - Stores the processed data in an SQLite database.

3. **API**: A Flask-based RESTful API that:
   - Provides an endpoint to fetch aggregated weather data by country.
   - Returns the latest weather conditions and average temperature for cities in the specified country.

## **Setup Instructions**

### **Prerequisites**

- **Python 3.8+**
- **AWS Account**: For using AWS SQS.
- **SQLite**: Integrated with Python; no additional installation required.
- **WeatherAPI Account**: For accessing weather data.

### **Installation**

1. **Clone the Repository**

   ```bash
   git clone https://github.com/SimShig/WeatherAPI.git
   cd WeatherAPI
2. **Create and Activate a Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install Dependencies**

     ```bash
    pip install -r requirements.txt

4. **Environment Variables**
   
    Create a .env file in the root directory with the following environment variables:

    ```plaintext
    WEATHER_API_KEY=your_weather_api_key_here
    SQS_QUEUE_URL=https://sqs.your-region.amazonaws.com/your-account-id/exercise-exodus
    DB_NAME =your db desired name
5. **Usage**
   
    Running the processes:
      ```bash

     python scheduler.py
     python processor.py
     python api.py

  
  Access the API via http://127.0.0.1:5000/exercise/<location_country>.


  **Enjoy!**
