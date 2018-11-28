from flask import Blueprint
from bs4 import BeautifulSoup
import calendar
from collections import Counter
import csv
import datetime
import numpy
import os
import requests
from flask import redirect
import dotenv
from pymongo import MongoClient
import pandas
import officials

dotenv.load_dotenv(verbose=True)
today = datetime.date.today()
register = Blueprint("register", __name__, url_prefix="/register")


def create_collection():
    client = MongoClient('localhost', 27017)
    db = client['analytic_database']
    collection = db['analytic_database']
    return collection


@register.route('/')
def insert_collection():
    session = login_to_homelog()
    source_file = get_csv(session)
    sending_dict = extract_sender(source_file)
    result_dict = count_officials_sending(sending_dict)
    result_for_sending = {'month': '%d' % (today.month-1), 'body': result_dict}
    create_collection().insert_one(result_for_sending)
    record = create_collection().find_one({"month": str(10)})
    print(record)
    return redirect('/')


@register.route('/update/<month>')
def updata_collection(month=None):
    session = login_to_homelog()
    source_file = get_csv(session, month=int(month))
    sending_dict = extract_sender(source_file)
    result_dict = count_officials_sending(sending_dict)
    create_collection().remove({'month': str(month)})
    create_collection().insert_one({'month': str(month), 'body': result_dict})
    record = create_collection().find_one({"month": str(month)})
    print(record)
    # print(result_for_sending)
    # return ("updata completed: %s"%record)
    return redirect('/')


@register.route('/badge_kind/update/<month>')
def insert_sender_receiver_badgekind(month=None):
    month = month or today.month-1
    session = login_to_homelog()
    source_file = get_csv(session, month=int(month))
    sending_list = create_all_data_dict(source_file)
    # print(sending_list)
    #TODO:Change logic insert all data record and extract per scean
    result_dict = extract_sender_receiver_badgekind(sending_list)
    result_for_sending = {'month': 'bk_%d' % int(month), 'body': result_dict}
    create_collection().remove({'month': 'bk_%d' % int(month)})
    create_collection().insert_one(result_for_sending)
    record = create_collection().find_one({"month": 'bk_%d' % int(month)})
    print('record :%s' % record)
    return redirect('/')


def extract_sender_receiver_badgekind(sending_list):
    sender_receiver_badgekind_list = []
    for row in sending_list:
        temp_dict = {}
        temp_dict['送信者名'] = row['送信者名']
        temp_dict['受信者名'] = row['受信者名']
        temp_dict['贈ったバッジ'] = row['贈ったバッジ']
        temp_dict['メッセージ'] = row['メッセージ']
        sender_receiver_badgekind_list.append(temp_dict)
    # print(sender_receiver_badgekind_list)
    return sender_receiver_badgekind_list


def login_to_homelog():
    url = os.environ.get('URL')
    login_url = os.environ.get('LOGIN_URL')
    user_id = os.environ.get('USER_ID')
    password = os.environ.get('PASSWORD')

    login_payload = {
        'utf-8': '✓',
        'admin_admin_user[email]': user_id,
        'admin_admin_user[password]': password
    }

    session = requests.Session()
    r = session.get(url)
    soup = BeautifulSoup(r.text, features='html.parser')
    auth_token = soup.find(attrs={'name': 'authenticity_token'}).get('value')
    login_payload['authenticity_token'] = auth_token

    session.post(login_url, data=login_payload)
    return session


def get_csv(session, month=None):
    month = month or today.month-1
    datasheet = os.environ.get('DATA_URL')
    base_calender = "%s/%d" % (today.year, month)
    date_from = '%s/01' % base_calender
    print(date_from)
    _, end_month = calendar.monthrange(today.year, month)
    date_to = '%s/%d' % (base_calender, end_month)
    print(date_to)
    sheet_payload = {
        'csv[date_from]': date_from,
        'csv[date_to]': date_to,
        'csv[badge_id]': ''
    }
    response = session.get(datasheet, data=sheet_payload)
    print(response.status_code)

    content_disposition = response.headers['Content-Disposition']
    attribute = 'filename='
    file_name = content_disposition[content_disposition.find(attribute) +
                                  len(attribute):].replace('\"', '')
    save_path = os.path.join(os.getcwd(), "Data", file_name)

    with open(save_path, 'wb') as save_file_name:
        save_file_name.write(response.content)
    return save_path


def extract_sender(source_file):
    with open(source_file, 'r', encoding='CP932') as fin:
        reader = pandas.read_csv(fin, usecols=[1])
        processed_list = numpy.ravel(reader.values)
        counter = Counter(processed_list)
        num_list = {}
        for word, cnt in counter.most_common():
            num_list[word] = cnt
        return num_list


def create_all_data_dict(source_file):
    with open(source_file, 'r', encoding='CP932') as fin:
        reader = csv.DictReader(fin)
        print(reader)
        data=[]
        for row in reader:
            data.append(row)
        return data


def count_officials_sending(sending_dict):
    official_list = officials.namelist
    officials_send_count_dict = []
    for person in official_list:
        tmp = {}
        try:
            tmp["name"] = person
            tmp["count"] = sending_dict[person]
            officials_send_count_dict.append(tmp)
        except:
            tmp["name"] = person
            tmp["count"] = 0
            officials_send_count_dict.append(tmp)
    return(officials_send_count_dict)


if __name__ == '__main__':
    print('start')
    insert_sender_receiver_badgekind()
    print('end')
