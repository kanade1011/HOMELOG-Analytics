from flask import Blueprint, render_template
import datetime
from api import result_getter

view = Blueprint("view", __name__, url_prefix="/result")
today = datetime.date.today()


@view.route('/<specified_month>')
def view_month_summry(specified_month=None):
    month = specified_month or '%s' % (today.month - 1)
    result = result_getter.result_getter(month=month)
    print(result)
    return render_template('month_summry.html', result=result, month=month)


@view.route('/')
def view_this_month_summry():
    month = '%s' % (today.month - 1)
    result = result_getter.result_getter(month=month)
    print(result)
    return render_template('month_summry.html', result=result, month=month)


if __name__ == '__main__':
    view_month_summry()
