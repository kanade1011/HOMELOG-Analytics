import os
import pandas
from services import result_creater, util


def download_monthly_sheet(year, month):
    result = result_creater.monthly_data_getter(year, month)
    print('downloaded: %s' % result)
    index = list()
    counter = list()
    for buffer in result:
        index.append(buffer['name'])
        counter.append(buffer['count'])
    # print(index)
    df = pandas.DataFrame(counter, index=index)
    filename = util.create_filename(month)
    data_dir = os.path.join(os.getcwd(), 'Data', filename)
    # print(data_dir)
    df.to_excel(data_dir, sheet_name='new_sheet_name', header=False)


def download_4q_mvp_analytics(result):
    name = list()
    total = list()
    sending = list()
    receiving = list()
    for buffer in result:
        name.append(buffer['name'])
        total.append(buffer['total'])
        sending.append(buffer['sending'])
        receiving.append(buffer['receiving'])
    df = pandas.DataFrame({'total': total,
                           'sending': sending,
                           'receiving': receiving},
                          index=name)
    # print("data:\n%s" % df)
    data_dir = os.path.join(os.getcwd(), 'Data', 'mvp_4Q_list.xlsx')
    df.to_excel(data_dir, sheet_name='mvp_4Q_list', header=True)
    print('download succeeded')
