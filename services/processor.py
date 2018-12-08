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


def result_getter(year, month):
    record = create_collection().find_one({'y-month': '%s/%s' % (year, month)})
    return record['body']


def get_update_data():
    last_updated = create_collection().find_one({'last_update': True})
    print(last_updated)
    return last_updated


def create_sender_dict(year, month):
    data = result_getter(year, month)
    sender = []
    # print(data)
    for rec in data:
        sender.append(rec['送信者名'])
    processed_list = numpy.ravel(sender)
    counter = Counter(processed_list)
    sender_dict = {}
    for word, cnt in counter.most_common():
        sender_dict[word] = cnt
    # print(sender_dict)
    return sender_dict


def extract_sender_receiver_badgekind(year, month):
    sending_list = result_getter(year, month)
    sender_receiver_badgekind_list = []
    for row in sending_list:
        temp_dict = {}
        temp_dict['送信者名'] = row['送信者名']
        temp_dict['受信者名'] = row['受信者名']
        temp_dict['贈ったバッジ'] = row['贈ったバッジ']
        temp_dict['メッセージ'] = row['メッセージ']
        sender_receiver_badgekind_list.append(temp_dict)
    return sender_receiver_badgekind_list


def count_officials_sending(year, month):
    sender_dict = create_sender_dict(year, month)
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


def create_filename(month):
    month = int(month)
    month_name = ""
    if month == 1:
        month_name = "January"
    elif month == 2:
        month_name = "February"
    elif month == 3:
        month_name = "March"
    elif month == 4:
        month_name = "April"
    elif month == 5:
        month_name = "May"
    elif month == 6:
        month_name = "June"
    elif month == 7:
        month_name = "July"
    elif month == 8:
        month_name = "August"
    elif month == 9:
        month_name = "September"
    elif month == 10:
        month_name = "October"
    elif month == 11:
        month_name = "November"
    elif month == 12:
        month_name = "December"

    basa_name = "%s_result.xlsx" % month_name
    return basa_name


if __name__ == '__main__':
    # print(count_officials_sending(10))
    print(count_officials_sending(10))
