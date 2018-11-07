'''
Created on 2018/10/27

@author: Administrator
'''
from bs4 import BeautifulSoup
from collections import Counter
import datetime
import dotenv
import numpy
import os
import requests

import pandas
from pandas.tests.io.parser import usecols

import officials

dotenv.load_dotenv(verbose=True)


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

    response = session.post(login_url, data=login_payload)
    return session


def get_csv(session):
    datasheet = os.environ.get('DATA_URL')
    sheet_payload = {
        'csv[date_from]': '2018/10/01',
        'csv[date_to]': '2018/10/31',
        'csv[badge_id]': ''
    }
    response = session.get(datasheet, data=sheet_payload)
    print(response.status_code)

    contentType = response.headers['Content-Type']
    contentDisposition = response.headers['Content-Disposition']
    attribute = 'filename='
    file_name = contentDisposition[contentDisposition.find(attribute) +
                                  len(attribute):].replace('\"', '')

    save_file_name = datetime.datetime.now().strftime('%Y%m%d') + file_name
    save_file_path = os.path.join(os.getcwd(), "Data", file_name)
    with open(save_file_path, 'wb') as saveFile:
        saveFile.write(response.content)
    return save_file_path


def extract_sender(source_file):
    with open(source_file, 'r', encoding='CP932') as fin:
        reader = pandas.read_csv(fin, usecols=[1])
        processed_list = numpy.ravel(reader.values)
        counter = Counter(processed_list)
        num_list = {}
        for word, cnt in counter.most_common():
            num_list[word] = cnt
        return num_list


def count_officials_sending(sending_dict):
    official_list = officials.namelist
    officials_send_counter = {}
    for person in official_list:
        try:
            officials_send_counter[person] = sending_dict[person]
        except:
            officials_send_counter[person] = 0
    print(officials_send_counter)


if __name__ == '__main__':
    print('start')
    session = login_to_homelog()
    source_file = get_csv(session)
    sending_dict = extract_sender(source_file)
    count_officials_sending(sending_dict)
    print('end')
