import json
from datetime import datetime
from consts import FARM_AREA

"""
this file is used to store initial data in database
"""


def store_initial_data():
    """
    this function is used to store initial data in database
    :return: None
    """
    from real_time_database import RealTimeDatabase
    data_base = RealTimeDatabase()
    # load data from json file
    for area in FARM_AREA:
        data_bio = json.load(open(rf"../stormglass_api/data/{area}.json"))
        data_bio = extract_one_entry(data_bio)
        data_bio.pop("time", None) # remove time key so we will store only the data
        data_base.create_data(area, data_bio)
        data_weather = json.load(open(rf"../stormglass_api/data/{area}_weather.json"))
        # extract one entry per day
        data_weather = extract_one_entry(data_weather)
        data_weather.pop("time", None) # remove time key so we will store only the data
        # add weather data to database
        data_base.update_data(area, data_weather)


def extract_one_entry(data):
    """
    this function is used to extract one entry from initial data
    this is done to reduce the size of the data stored in the database
    it is only used for the initial data.
    :param data:
    :return:
    """
    result = data["hours"][-1]
    return result


if __name__ == '__main__':
    store_initial_data()