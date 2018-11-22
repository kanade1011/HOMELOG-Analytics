from flask import Blueprint
from bs4 import BeautifulSoup
import calendar
from collections import Counter
import datetime
import numpy
import os
import json
import requests
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
    # create_collection().remove({'month': "10"})
    record = create_collection().find_one({"month": str(10)})
    print(record)
    # print(result_for_sending)
    return ("completed: %s" % result_for_sending)


@register.route('/updata/<month>')
def updata_collection(month=None):
    session = login_to_homelog()
    source_file = get_csv(session)
    sending_dict = extract_sender(source_file)
    result_dict = count_officials_sending(sending_dict)
    create_collection().remove({'month': str(month)})
    create_collection().insert_one({'month': str(month), 'body': result_dict})
    record = create_collection().find_one({"month": str(month)})
    print(record)
    # print(result_for_sending)
    return ("updata completed: %s"%record)


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

    contentDisposition = response.headers['Content-Disposition']
    attribute = 'filename='
    file_name = contentDisposition[contentDisposition.find(attribute) +
                                  len(attribute):].replace('\"', '')
    save_path = os.path.join(os.getcwd(), "Data", file_name)

    # save_path = tempfile.NamedTemporaryFile(mode='w', suffix='.csv')
    with open(save_path, 'wb') as save_file_name:
        save_file_name.write(response.content)
    return save_path
    # fin = tempfile.mkstemp()
    # fin.write(response.content)
    # print(fin.name)
    # return fin.name


def extract_sender(source_file):
    with open(source_file, 'r', encoding='CP932') as fin:
        reader = pandas.read_csv(fin, usecols=[1])
        processed_list = numpy.ravel(reader.values)
        counter = Counter(processed_list)
        num_list = {}
        for word, cnt in counter.most_common():
            # print("word:%s, cnt:%s" % (word, cnt))
            num_list[word] = cnt
            # print(num_list)
        return num_list


def count_officials_sending(sending_dict):
    official_list = officials.namelist
    officials_send_count_dict = []
    for person in official_list:
        tmp = {}
        try:
            tmp["name"] = person
            tmp["count"] = sending_dict[person]
            officials_send_count_dict.append(tmp)
            # officials_send_count_dict[person] = sending_dict[person]
        except:
            # officials_send_count_dict[person] = 0
            pass
    # print(officials_send_count_dict)
    return(officials_send_count_dict)


if __name__ == '__main__':
    print('start')
    insert_collection()
    print('end')
