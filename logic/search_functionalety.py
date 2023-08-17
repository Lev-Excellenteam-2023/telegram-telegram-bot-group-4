"""
this file is used to search the database with the given parameters
"""
import asyncio
import logging
from typing import Dict
from consts import *
from data_base.real_time_database import RealTimeDatabase


async def is_suitable_location (db, area, params:Dict[str, float] ):
    """
    this function is used to check if the given parameters are suitable for the given area.
    :param db: database object.
    :param area: area to check.
    :param params: dictionary of parameters to check with the given area.
    :return: True if the given parameters are suitable for the given area, False otherwise.
    """
    try:
        data = db.read_data(area)
        if data is None:
            return False
        for key_param in params.keys():
            if data[key_param] != params[key_param]:
                return False
        return True
    except Exception as e:
        logging.error(e)


async def search_parmeter_in_different_sources(data_base_parameter, parameter):
    """
    this function is used to search the database with the given parameters
    :param dict: dictionary of parameters
    :return: None
    """
    try:
        if isinstance(data_base_parameter, dict):
            for source in data_base_parameter.keys():
                if data_base_parameter[source] == parameter:
                    return True
            return False
        else:
            return data_base_parameter == parameter
    except Exception as e:
        logging.error(e)


async def search_suitable_location(*args, **kwargs):
    """
    this function is used to search the database with the given parameters
    :param args: list of parameters
    :param kwargs: dictionary of parameters
    :return: None
    """
    try:
        res = []
        db = RealTimeDatabase()
        for area in FARM_AREA:
            if await is_suitable_location(db, area, kwargs):
                res.append(area)
        return res
    except Exception as e:
        logging.error(e)
