import os
from pymongo import MongoClient
import numpy
from collections import Counter
import officials


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


def result_getter(month):
    record = create_collection().find_one({"month": str(month)})
    return record['body']


def create_sender_dict(month):
    data = result_getter(month)
    sender = []
    print(data)
    for rec in data:
        sender.append(rec['送信者名'])
    processed_list = numpy.ravel(sender)
    counter = Counter(processed_list)
    sender_dict = {}
    for word, cnt in counter.most_common():
        sender_dict[word] = cnt
    print(sender_dict)
    return sender_dict


def extract_sender_receiver_badgekind(month):
    sending_list = result_getter(month)
    sender_receiver_badgekind_list = []
    for row in sending_list:
        temp_dict = {}
        temp_dict['送信者名'] = row['送信者名']
        temp_dict['受信者名'] = row['受信者名']
        temp_dict['贈ったバッジ'] = row['贈ったバッジ']
        temp_dict['メッセージ'] = row['メッセージ']
        sender_receiver_badgekind_list.append(temp_dict)
    return sender_receiver_badgekind_list


def count_officials_sending(month):
    sender_dict = create_sender_dict(month)
    official_list = officials.namelist
    officials_send_count_dict = []
    for person in official_list:
        tmp = {}
        try:
            tmp["name"] = person
            tmp["count"] = sender_dict[person]
            officials_send_count_dict.append(tmp)
        except:
            tmp["name"] = person
            tmp["count"] = 0
            officials_send_count_dict.append(tmp)
    return officials_send_count_dict


if __name__ == '__main__':
    # print(count_officials_sending(10))
    print(count_officials_sending(10))
