from flask import Flask
from pymongo import MongoClient
import services.batch_service as service

# app = Flask(__name__)


def create_collection():
    client = MongoClient('localhost', 27017)
    db = client['analytic_database']
    collection = db['analytic_database']
    return collection


collection = create_collection()
post = service.create_collection()

collection.insert_one(post)

record = collection.find_one({"month": "10"})
print(record['body'])