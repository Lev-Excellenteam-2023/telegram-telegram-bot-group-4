import data_base_intialization as dbi
import firebase_admin as fa
from firebase_admin import db


def search_city(city_name: str) -> dict:
    ref = dbi.initialize_database()
    cities = ref.child("cities").get()
    for city in cities:
        if city["name"] == city_name:
            return city
    return {}


def add_city(city_name: str, city_id: int, city_data: dict) -> None:
    ref = dbi.initialize_database()
    ref.child("cities").child(city_id).set(city_data)

