from flask import Blueprint
from bs4 import BeautifulSoup
import calendar
import csv
import datetime
import os
import requests
import tempfile
from flask import redirect
import dotenv
from pymongo import MongoClient

dotenv.load_dotenv(verbose=True)
today = datetime.date.today()
register = Blueprint("register", __name__, url_prefix="/register")


def create_collection():
    client = MongoClient('localhost', 27017)
    db = client['analytic_database']
    collection = db['analytic_database']
    return collection


@register.route('/<month>')
def insert_monthly_record(month=None):
    session = login_to_homelog()
    csv_record = get_csv(session, month=int(month))
    sending_list = create_all_data_list(csv_record)
    result_for_sending = {'month': '%d' % int(month), 'body': sending_list}
    print(result_for_sending)
    create_collection().remove({'month': str(month)})
    create_collection().insert_one(result_for_sending)
    return redirect('/')


def create_all_data_list(csv_record):
    tmp = tempfile.NamedTemporaryFile().name
    with open(tmp, 'w') as f:
        f.write(csv_record)

    with open(tmp, 'r', encoding='CP932') as fin:
        reader = csv.DictReader(fin)
        print(reader)
        data = []
        for row in reader:
            data.append(row)
        return data


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
    month = month or today.month - 1
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
    csv_record = response.content.decode('CP932')
    return csv_record


if __name__ == '__main__':
    print('start')
    # insert_monthly_record("10")
    print('end')
