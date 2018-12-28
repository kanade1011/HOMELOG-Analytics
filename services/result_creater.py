import os
from pymongo import MongoClient
import officials
from services import processor


def create_collection():
    MONGO_URL = os.environ.get('MONGOHQ_URL')
    if MONGO_URL:
        client = MongoClient(MONGO_URL)
        db = client['analytic_database']
    else:
        client = MongoClient('localhost', 27017)
        db = client['analytic_database']
    collection = db['analytic_database']
    return collection


def monthly_data_getter(year, month):
    return processor.count_officials_sending(year, month)


def person_record_getter(person=None):
    person = person or '小澤 健治'
    year = 2018
    month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    report = []
    for month in month_list:
        try:
            monthly_date = processor.count_officials_sending(year, month)
            print('%d monthly_data: %s' % (month, monthly_date))
            for persons in monthly_date:
                if persons['name'] == person:
                    dictionary = {}
                    dictionary['month'] = month
                    dictionary['badge'] = persons['count']
                    # print(dictionary)
                    report.append(dictionary)
        except:
            print('pass data: %d', month)
            dictionary = {}
            dictionary['month'] = month
            dictionary['badge'] = 0
            # print(dictionary)
            report.append(dictionary)
    # print(report)
    return report


def all_person_record_getter():
    month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    year = 2018
    personal_sending_list = []
    for person in officials.namelist:
        report = [{'Name': person}]
        for month in month_list:
            try:
                month_data = processor.count_officials_sending(year, month)
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
        personal_sending_list.append(report)
    # print(personal_sending_list)
    return personal_sending_list


if __name__ == '__main__':
    all_person_record_getter()


def result_getter(year, month):
    record = create_collection().find_one({'y-month': '%s/%s' % (year, month)})
    return record['body']


def get_update_data():
    last_updated = create_collection().find_one({'last_update': True})
    print(last_updated)
    return last_updated