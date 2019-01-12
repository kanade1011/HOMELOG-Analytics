import numpy
from collections import Counter
from services import result_creater, processor


def mvp_analyze(year, start_month, fin_month):
    sender_list = count_badge_number(year, 'sending', start_month, fin_month)
    receiver_list = count_badge_number(year, 'receiving', start_month, fin_month)
    sending_and_receiving_list = list()
    for sender in sender_list:
        for receiver in receiver_list:
            if sender['name'] == receiver['name']:
                sender['receiving'] = receiver['receiving']
                sender['total'] = int(receiver['receiving'])+int(sender['sending'])
                sending_and_receiving_list.append(sender)
    print("mvp_analyzer return %s" % sending_and_receiving_list)
    sending_and_receiving_list.sort(key=lambda x: x['total'])
    sending_and_receiving_list.reverse()
    return sending_and_receiving_list


def mvp_analyze2(year, month, badge, type):
    """

    :param year:
    :param month:
    :param badge:
    :param type:
    :return:
    """
    result_type = processor.type_check_send_or_receive(type)
    receive_result = result_creater.result_getter(year, month)
    print("receive_result %s" % receive_result)

    count_list = list()
    for result in receive_result:
        if result['贈ったバッジ'] == badge:
            count_list.append(result[result_type])
    processed_list = numpy.ravel(count_list)
    counter = Counter(processed_list)

    receiving_and_badge_count_list = list()
    for word, cnt in counter.most_common():
        default_dict = dict()
        default_dict['name'] = word
        default_dict['count'] = cnt
        receiving_and_badge_count_list.append(default_dict)
    print("receiving_and_badge_count_list: %s" % receiving_and_badge_count_list)
    return receiving_and_badge_count_list


def _get_name_list_sending_or_receiving(year, analytic_kind, start_month, fin_month):
    results = list()
    months = list()
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


def count_badge_number(year, analytic_kind, start_month, fin_month):
    results = _get_name_list_sending_or_receiving(year, analytic_kind, int(start_month), int(fin_month))
    counter = Counter(results)
    counter_list = list()
    for word, cnt in counter.most_common():
        counter_dict = dict()
        counter_dict['name'] = word
        counter_dict[analytic_kind] = cnt
        counter_list.append(counter_dict)
    print('count_badgenumber return: %s \nkind: %s' % (counter_list, analytic_kind))
    return counter_list
