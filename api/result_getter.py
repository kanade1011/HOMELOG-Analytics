from flask import Blueprint

from pymongo import MongoClient

api = Blueprint("result_getter", __name__, url_prefix="/api")


def create_collection():
    client = MongoClient('localhost', 27017)
    db = client['analytic_database']
    collection = db['analytic_database']
    return collection


collection = create_collection()


@api.route('/<month>')
def result_getter(month=None):
    record = collection.find_one({"month": month})
    return str(record['body'])