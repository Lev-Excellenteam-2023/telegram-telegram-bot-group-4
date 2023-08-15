import firebase_admin
from firebase_admin import db, credentials


def initialize_database() -> db.Reference:
    # authentication to firebase
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {"databaseURL": "https://agriculture-telegram-bot-default-rtdb.firebaseio.com/"})
    ref = db.reference("/")
    return ref
