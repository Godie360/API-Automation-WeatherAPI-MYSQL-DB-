import requests
import json
import mysql.connector
from datetime import datetime

# Function to create a connection to MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='godie360',
            database='weather_database'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except mysql.connector.Error as e:
        print("Error: ", e)
        return None


# Inserting data into the table
def insert_data(cursor, temperature, weather_text, date, location):
    try:
        cursor.execute('''
            INSERT INTO weather_data (temperature, weather_text, date, location)
            VALUES (%s, %s, %s, %s)
        ''', (temperature, weather_text, date, location))
        print("DATA INSERTED SUCCESSFULLY")
    except mysql.connector.Error as e:
        print("Error inserting data: ", e)

# Function to commit changes and close the connection
def commit_and_close(connection):
    if connection:
        connection.commit()
        connection.close()
        print("Connection closed")

# Accuweather Api key and location key
api_key = 'zNyYRqDYWsekpPl8e088OmWpfxCGl4SH'
location_key = '314124'

# AccuWeather API URL
url = f'http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}'

# Make a request to the API
response = requests.get(url)

if response.status_code == 200:
    try:
        # Parse the JSON response
        data = response.json()

        # Check if the response is a non-empty list
        if data and isinstance(data, list) and len(data) > 0:
            # Get the temperature and weather text
            temperature = data[0]['Temperature']['Metric']['Value']
            weather_text = data[0]['WeatherText']
            date = data[0]['LocalObservationDateTime']
            location = 'Mtwara'

            # Create a connection and cursor to the MySQL database
            connection = create_connection()
            if connection:
                cursor = connection.cursor()

                # Insert data into the table
                insert_data(cursor, temperature, weather_text, date, location)

                commit_and_close(connection)
        else:
            print("Invalid response format or empty data.")
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
else:
    print("Request failed with status code:", response.status_code)
