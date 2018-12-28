import os
import pandas
from services import result_creater, util


def download_monthly_sheet(year, month):
    result = result_creater.monthly_data_getter(year, month)
    print('downloaded: %s' % result)
    index = []
    counter = []
    for buffer in result:
        index.append(buffer['name'])
        counter.append(buffer['count'])
    # print(index)
    df = pandas.DataFrame(counter, index=index)
    filename = util.create_filename(month)
    data_dir = os.path.join(os.getcwd(), 'Data', filename)
    # print(data_dir)
    df.to_excel(data_dir, sheet_name='new_sheet_name', header=False)