import numpy
from collections import Counter
import officials
from services import result_creater


def create_sender_dict(year, month):
    data = result_creater.result_getter(year, month)
    sender = list()
    # print(data)
    for rec in data:
        sender.append(rec['送信者名'])
    processed_list = numpy.ravel(sender)
    counter = Counter(processed_list)
    sender_dict = dict()
    for word, cnt in counter.most_common():
        sender_dict[word] = cnt
    # print(sender_dict)
    return sender_dict


def extract_sender_receiver_badgekind(year, month):
    sending_list = result_creater.result_getter(year, month)
    sender_receiver_badgekind_list = list()
    for sending in sending_list:
        temp_dict = dict()
        temp_dict['送信者名'] = sending['送信者名']
        temp_dict['受信者名'] = sending['受信者名']
        temp_dict['贈ったバッジ'] = sending['贈ったバッジ']
        temp_dict['メッセージ'] = sending['メッセージ']
        sender_receiver_badgekind_list.append(temp_dict)
    return sender_receiver_badgekind_list


def count_officials_sending(year, month):
    sender_dict = create_sender_dict(year, month)
    official_list = officials.namelist
    officials_send_count_list = list()
    for person in official_list:
        tmp = dict()
        try:
            tmp['name'] = person
            tmp['count'] = sender_dict[person]
            officials_send_count_list.append(tmp)
        except:
            tmp['name'] = person
            tmp['count'] = 0
            officials_send_count_list.append(tmp)
    return officials_send_count_list


def badgekind_getter(year, month, badge_name):
    record = result_creater.result_getter(year, month)
    reslut_list = []
    for row in record:
        if row['贈ったバッジ'] == badge_name:
            reslut_list.append(row)
    return reslut_list


if __name__ == '__main__':
    # print(count_officials_sending(2018, 10))
    # count_sending(2018)
    mvp_analyze(2018, 7, 11)