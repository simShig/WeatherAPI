from flask import Flask, jsonify
import sqlite3
from collections import OrderedDict


app = Flask(__name__)


def calc_city_props(rows):
    '''
    process rows for needed data (temp - avarage, condition - last)
    :param rows: data from DB filtered by country
    :return: cities data (dict where each item is a city in the given country)
    '''
    cities_data = {}
    for row in rows:
        city = row[0]
        temp_c = row[3]
        condition_text = row[4]
        localtime = row[2]

        if city not in cities_data:
            cities_data[city] = {
                "total_temp": 0,
                "count": 0,
                "latest_time": localtime,
                "latest_condition_text": condition_text
            }

        cities_data[city]["total_temp"] += temp_c
        cities_data[city]["count"] += 1

        if localtime > cities_data[city]["latest_time"]:
            cities_data[city]["latest_time"] = localtime
            cities_data[city]["latest_condition_text"] = condition_text

    return cities_data

def get_weather_data_by_country(country):
    '''
    query the DB and create the requiered agragated JSON
    :param country: which counrty is our point of interest
    :return: JSON formatted list of agragated data
    '''
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT location_name, location_country, location_localtime, temp_c, condition_text
    FROM weather
    WHERE location_country = ?
    ORDER BY location_name, location_localtime
    ''', (country,))


    rows = cursor.fetchall()
    conn.close()

    # print (rows)

    cities = calc_city_props(rows)
    # fetched rows to JSON format

    result = []
    for city, data in cities.items():
        result.append(OrderedDict({
            "city": city,
            "average_temp_c": round(data["total_temp"] / data["count"],4),
            "lastest_condition_text": data["latest_condition_text"]
        }))

    return result

# API route:
@app.route('/exercise/<location_country>', methods=['GET'])
def get_weather_by_country(location_country):
    '''
    encapsulation for get_weather_data_by_country (for error handeling purposes)
    :param location_country: the country we are intrested in (by the URL)
    :return: JSONified data | error data
    '''

    try:
        weather_data = get_weather_data_by_country(location_country)
        if not weather_data:
            return jsonify({f"message": f"No data found for the specified country ({location_country})"}), 404
        return jsonify(weather_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
