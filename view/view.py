from flask import Blueprint, render_template
import datetime
import json
from api import result_getter

view = Blueprint("view", __name__, url_prefix="/result")
today = datetime.date.today()


@view.route('/')
def view_month_summry():
    result = result_getter.result_getter(month='%s'%(today.month-1))
    # return (result)
    print(type(result))
    print(result)
    # json_result = json.dumps(result, ensure_ascii=False)
    # print(json_result)
    return render_template('month_summry.html', result=result)


if __name__ == '__main__':
    view_month_summry()