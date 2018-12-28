import numpy
from collections import Counter
import officials
from services import result_creater


def _get_name_list_sending_or_receiving(year, analytic_kind, start_month, fin_month):
    results = []
    months = []
    kind = ''

    for index in range(fin_month-start_month+1):
        months.append(start_month)
        start_month += 1
    print("months: %s" % months)

    if analytic_kind == "sending":
        kind = '送信者名'
    elif analytic_kind == 'receiving':
        kind = '受信者名'
    for month in months:
        result = result_creater.result_getter(year, month)
        for badge in result:
            results.append(badge[kind])
    print('get_name_list_sending_or_receiving return: %s\nkind: %s' % (results, analytic_kind))
    return results


def mvp_analyze(year, start_month, fin_month):
    sender_list = count_badge_number(year, 'sending', start_month, fin_month)
    receiver_list = count_badge_number(year, 'receiving', start_month, fin_month)
    sending_and_receiving_list = []
    for sender in sender_list:
        for receiver in receiver_list:
            if sender['name'] == receiver['name']:
                sender['receiving'] = receiver['receiving']
                sender['total'] = int(receiver['receiving'])+int(sender['sending'])
                sending_and_receiving_list.append(sender)
    print("mvp_analyzer return %s" % sending_and_receiving_list)
    return sending_and_receiving_list


def count_badge_number(year, analytic_kind, start_month, fin_month):
    results = _get_name_list_sending_or_receiving(year, analytic_kind, int(start_month), int(fin_month))
    counter = Counter(results)
    conter_list = []
    for word, cnt in counter.most_common():
        conter_dict = {}
        conter_dict['name'] = word
        conter_dict[analytic_kind] = cnt
        conter_list.append(conter_dict)
    print('count_badgenumber return: %s \nkind: %s' % (conter_list, analytic_kind))
    return conter_list


def create_sender_dict(year, month):
    data = result_creater.result_getter(year, month)
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
    sending_list = result_creater.result_getter(year, month)
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
    officials_send_count_list = []
    for person in official_list:
        tmp = {}
        try:
            tmp['name'] = person
            tmp['count'] = sender_dict[person]
            officials_send_count_list.append(tmp)
        except:
            tmp['name'] = person
            tmp['count'] = 0
            officials_send_count_list.append(tmp)
    return officials_send_count_list


def create_filename(month):
    month = int(month)
    month_name = ''
    if month == 1:
        month_name = 'January'
    elif month == 2:
        month_name = 'February'
    elif month == 3:
        month_name = 'March'
    elif month == 4:
        month_name = 'April'
    elif month == 5:
        month_name = 'May'
    elif month == 6:
        month_name = 'June'
    elif month == 7:
        month_name = 'July'
    elif month == 8:
        month_name = 'August'
    elif month == 9:
        month_name = 'September'
    elif month == 10:
        month_name = 'October'
    elif month == 11:
        month_name = 'November'
    elif month == 12:
        month_name = 'December'

    basa_name = '%s_result.xlsx' % month_name
    return basa_name


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