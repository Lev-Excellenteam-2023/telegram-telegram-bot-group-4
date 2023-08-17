import firebase_admin
from firebase_admin import db, credentials
from consts import DATA_BASE_URL, CERTIFICATE_PATH


class RealTimeDatabase:
    """
    this class is used to interact with the real time database
    """
    def __init__(self):
        self.database = initialize_database()

    def create_data(self, area, data):
        self.database.child(area).set(data)

    def read_data(self, area):
        return self.database.child(area).get()

    def update_data(self, area, data):
        self.database.child(area).update(data)

    def delete_data(self, area):
        self.database.child(area).delete()


def initialize_database() -> db.Reference:
    """
    this function is used to initialize database
    :return: database root reference
    """
    # TODO: change certification to more secure one
    cred = credentials.Certificate(CERTIFICATE_PATH)
    firebase_admin.initialize_app(cred, {"databaseURL":DATA_BASE_URL })
    ref = db.reference("/")
    return ref
