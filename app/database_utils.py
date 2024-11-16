import time
from pymongo.errors import ConnectionFailure
from app.extensions import db


def wait_for_mongo():
    while True:
        try:
            db.client.admin.command('ping')
            print("MongoDB est prêt.")
            break
        except ConnectionFailure:
            print("MongoDB n'est pas disponible, nouvelle tentative dans 5 secondes...")
            time.sleep(5)
