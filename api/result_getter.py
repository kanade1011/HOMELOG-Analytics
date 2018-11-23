from flask import Blueprint
from pymongo import MongoClient
import officials

api = Blueprint("result_getter", __name__, url_prefix="/api")


def create_collection():
    client = MongoClient('localhost', 27017)
    db = client['analytic_database']
    collection = db['analytic_database']
    return collection


collection = create_collection()


@api.route('/<month>')
def result_getter(month=None):
    record = collection.find_one({"month": str(month)})
    return record['body']


@api.route('/<person>')
def person_record_getter(person=None):
    person = person or "小澤 健治"
    month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    report = []
    for month in month_list:
        try:
            rec = collection.find_one({"month": str(month)})
            month_data = rec['body']
            for persons in month_data:
                if persons['name'] == person:
                    dictionary = {}
                    dictionary['month'] = month
                    dictionary['badge'] = persons['count']
                    # print(dictionary)
                    report.append(dictionary)
        except:
            dictionary = {}
            dictionary['month'] = month
            dictionary['badge'] = 0
            # print(dictionary)
            report.append(dictionary)
    # print(report)
    return report


def all_person_record_getter():
    month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    personal_sending_list = []
    for person in officials.namelist:
        report = {'Name': person}
        for month in month_list:
            try:
                rec = collection.find_one({"month": str(month)})
                month_data = rec['body']
                for persons in month_data:
                    if persons['name'] == person:
                        report[month] = persons['count']
                        # print(month, persons['count'])
            except:
                report[month] = 0
        personal_sending_list.append(report)
    # print(personal_sending_list)
    return personal_sending_list


if __name__ == '__main__':
    person_record_getter()
