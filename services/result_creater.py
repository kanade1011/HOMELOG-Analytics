import officials
from services import processor


def badgekind_getter(month, badge_name):
    record = processor.result_getter(month)
    reslut_list = []
    for row in record:
        if row['贈ったバッジ'] == badge_name:
            reslut_list.append(row)
    return reslut_list


def monthly_data_getter(month):
    return processor.count_officials_sending(month)


def person_record_getter(person=None):
    person = person or "小澤 健治"
    month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    report = []
    for month in month_list:
        try:
            monthly_date = processor.count_officials_sending(month)
            print("%d monthly_data: %s" % (month, monthly_date))
            for persons in monthly_date:
                if persons['name'] == person:
                    dictionary = {}
                    dictionary['month'] = month
                    dictionary['badge'] = persons['count']
                    # print(dictionary)
                    report.append(dictionary)
        except:
            print("pass data: %d", month)
            dictionary = {}
            dictionary['month'] = month
            dictionary['badge'] = 0
            # print(dictionary)
            report.append(dictionary)
    # print(report)
    return report


def all_person_record_getter():
    month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    personal_sending_list = []
    for person in officials.namelist:
        report = [{'Name': person}]
        for month in month_list:
            try:
                month_data = processor.count_officials_sending(month)
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
