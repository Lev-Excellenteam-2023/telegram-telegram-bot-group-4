"""
this file is used to get data from stormglass api
used only for initial data collection
TODO: make an automated script to get data from stormglass api and store it in a database.
"""
import requests
import json
import datetime

# TODO: store api key in a secure place
# API_KEY = '333551e0-3b99-11ee-a654-0242ac130002-3335529e-3b99-11ee-a654-0242ac130002'
API_KEY = '243e5fa4-3c13-11ee-a654-0242ac130002-243e601c-3c13-11ee-a654-0242ac130002'
FARM_AREA = {
    "Upper Galilee": {"lat": 35.503194086263335, "lng": 32.892852451153814},
    "Lower Galilee": {"lat": 35.294, "lng": 32.701},
    "Southern Negev": {"lat": 35.57, "lng": 32.317222},
    "Northern Negev": {"lat": 35.57, "lng": 29.9861544},
    "Jordan Valley": {"lat": 35.57, "lng": 32.317222},
    "Hshfela Valley": {"lat": 34.816366340965, "lng": 31.9941801717},
    "Central district": {"lat": 32.031941, "lng": 34.858982}
}
START_DATE = "1/6/2023"
END_DATE = "12/6/2023"


def get_data ( lat, lng, start, end, endpoint: str, parms: list ) -> json:
    """
    this function is used to get data from stormglass api
    :param lat: latitude
    :param lng: longitude
    :param start: start date in unix timestamp
    :param end: end date in unix timestamp
    :param endpoint: api endpoint
    :param parms: list of parameters to get
    :return: json data
    """
    response = requests.get(
        endpoint,
        params={
            'lat': lat,
            'lng': lng,
            'params': ','.join(parms),
            'start': start,
            'end': end
        },
        headers={
            'Authorization': API_KEY
        }
    )
    json_data = response.json()
    return json_data


def store_data_to_file ( json_data, file_name='data' ):
    """
    this function is used to store data in a database
    :param json_data: json data
    :param file_name: file name
    :return: None
    """
    print(json_data)
    with open(file_name + '.json', 'w') as outfile:
        json.dump(json_data, outfile)


def date_to_unix_timestamp ( date_str ):
    """
    this function is used to convert date to unix timestamp
    :param date_str:  date in string format
    :return: unix timestamp
    """
    date_obj = datetime.datetime.strptime(date_str, '%m/%d/%Y')
    unix_timestamp = int(date_obj.timestamp())
    return unix_timestamp


def get_bio ( start_unix, end_unix ):
    """
    this function is used to get bio data from stormglass api
    :param start_unix: unix timestamp
    :param end_unix: unix timestamp
    :return: None
    """
    for area in FARM_AREA:
        json_data = get_data(FARM_AREA[area]["lat"], FARM_AREA[area]["lng"], start_unix, end_unix,
                             'https://api.stormglass.io/v2/bio/point',
                             ['soilMoisture', 'soilMoisture10cm', 'soilMoisture40cm',
                              'soilMoisture100cm', 'soilTemperature', 'soilTemperature10cm', 'soilTemperature40cm',
                              'soilTemperature100cm'])
        store_data_to_file(json_data, area + '_bio')


def get_weather ( start_unix, end_unix ):
    """
    this function is used to get weather data from stormglass api
    :param start_unix: unix timestamp
    `param end_unix: unix timestamp
    :return: None
    """
    for area in FARM_AREA:
        json_data = get_data(FARM_AREA[area]["lat"], FARM_AREA[area]["lng"], start_unix, end_unix,
                             'https://api.stormglass.io/v2/weather/point',
                             ['airTemperature', 'pressure', 'cloudCover', 'currentSpeed',
                              'humidity', 'windSpeed'])
        store_data_to_file(json_data, 'data/' + area + '_weather')


if __name__ == '__main__':
    start_unix = date_to_unix_timestamp(START_DATE)
    end_unix = date_to_unix_timestamp(END_DATE)
    get_bio(start_unix, end_unix)
    get_weather(start_unix, end_unix)
